from django.urls import path

from .views import CreatePaymentView, PaymentCallBackView, book_list, download_book_file

urlpatterns = [
    path("books-store/", book_list, name="book_list"),
    path(
        "create-payment/<uuid:book_uuid>/",
        CreatePaymentView.as_view(),
        name="create_payment",
    ),
    path(
        "payment-verify/",
        PaymentCallBackView.as_view(),
        name="payment_verify",
    ),
    path(
        "book/<uuid:book_uuid>/download/", download_book_file, name="download_book_file"
    ),
]
