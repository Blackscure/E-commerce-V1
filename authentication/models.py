from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager

from utils.choices import SEX, USER_TYPE

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=80, unique=True)
    sex = models.CharField(max_length=42, choices=SEX, default='male')
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    user_type = models.CharField(max_length=42, choices=USER_TYPE, default='customer')
   

