from django.db import models

from authentication.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)