from django.contrib.auth import get_user_model
from django.db import models

from core.mixins import AbstractTrack

User = get_user_model()


class Book(AbstractTrack):
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    author = models.CharField(max_length=255)
    book_file = models.FileField(upload_to="book_files/", blank=True, null=True)

    def __str__(self):
        return self.title


class Order(AbstractTrack):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255)
    razorpay_signature = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.razorpay_order_id
