from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="merchant")

    def __str__(self):
        return self.user.email

class Store(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="stores")
    open_date = models.DateField(auto_now_add=True)
