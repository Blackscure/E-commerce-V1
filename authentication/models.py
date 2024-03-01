from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from utils.choices import SEX, USER_TYPE

class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with additional fields.
    """

    email = models.EmailField(_('email address'), unique=True)
    sex = models.CharField(max_length=42, choices=SEX, default='male')
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    user_type = models.CharField(max_length=42, choices=USER_TYPE, default='customer')

    # Additional fields
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    # Override default username field
    username = models.CharField(_('username'), max_length=30, unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
