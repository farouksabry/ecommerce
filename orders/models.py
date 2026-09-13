from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

class Order(models.Model):
    ORDER_STATUS = [
        ("Ordered", "Ordered"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered")
    ]
    
    PAYMENT_METHOD = [
        ("VISA", "Visa"),
        ("CASH", "Cash")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=9, choices=ORDER_STATUS, default="Ordered")
    mobile = PhoneNumberField(null=True, blank=True)
    paid = models.BooleanField()
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
