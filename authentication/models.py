from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager

from utils.choices import SEX

# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    sex = models.CharField(max_length=42, choices=SEX, default='male')
    mobile_number = models.CharField(max_length=45, unique=True)
    status = models.BooleanField(default=True)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_customer = models.BooleanField(default=True)
