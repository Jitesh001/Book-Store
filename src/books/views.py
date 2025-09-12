import os

import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .models import Book, Order

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def book_list(request):
    user_orders = Order.objects.filter(
        user=request.user, book=OuterRef("pk"), is_paid=True
    )
    books = Book.objects.annotate(is_paid=Exists(user_orders))
    return render(request, "books/books_list.html", {"books": books})


@method_decorator(csrf_exempt, name="dispatch")
class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request, book_uuid):
        book = get_object_or_404(Book, uuid=book_uuid)
        data = {
            "amount": int(book.price * 100),
            "currency": "INR",
            "payment_capture": 1,
        }
        payment = client.order.create(data=data)
        Order.objects.create(
            user=request.user,
            book=book,
            razorpay_order_id=payment["id"],
        )
        return JsonResponse(
            {
                "order_id": payment["id"],
                "amount": int(book.price * 100),
                "book": book.title,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "razorpay_callback_url": settings.RAZORPAY_CALLBACK_URL,
                "user_full_name": "Jitesh Shewale",
                "user_email": "jitesh@gmail.com",
            }
        )


class PaymentCallBackView(View):
    def post(self, request):
        if "razorpay_signature" in request.POST:
            order_id = request.POST.get("razorpay_order_id")
            payment_id = request.POST.get("razorpay_payment_id")
            signature = request.POST.get("razorpay_signature")

            order = get_object_or_404(Order, razorpay_order_id=order_id)
            if client.utils.verify_payment_signature(
                {
                    "razorpay_order_id": order_id,
                    "razorpay_payment_id": payment_id,
                    "razorpay_signature": signature,
                }
            ):
                order.razorpay_payment_id = payment_id
                order.razorpay_signature = signature
                order.is_paid = True
                order.save()
                return JsonResponse({"status": "Payment successful"})
        return JsonResponse({"status": "Payment failed"})


def download_book_file(request, book_uuid):
    book = get_object_or_404(Book, uuid=book_uuid)
    if not book.book_file:
        raise Http404("Book PDF not found")

    file_path = book.book_file.path
    if not os.path.exists(file_path):
        raise Http404("File not found")

    with open(file_path, "rb") as f:
        response = FileResponse(
            f, as_attachment=True, filename=os.path.basename(file_path)
        )
    response["Content-Disposition"] = (
        f'attachment; filename="{os.path.basename(file_path)}"'
    )
    return response
