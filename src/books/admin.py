from django.contrib import admin

from .models import Book, Order


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "created", "book_file")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "created", "is_paid", "razorpay_order_id")
