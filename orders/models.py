from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

ORDER_STATUS = [
    ("ORDERED", "Ordered"),
    ("SHIPPED", "Shipped"),
    ("DELIVERED", "Delivered")
]

PAYMENT_METHOD = [
    ("VISA", "Visa"),
    ("CASH", "Cash")
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100)
    mobile = PhoneNumberField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=9, choices=ORDER_STATUS, default="ORDERED")

    @property
    def item_subtotal(self):
        return self.unit_price * self.quantity
