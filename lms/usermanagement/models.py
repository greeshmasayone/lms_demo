from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import DateBaseModel
from .managers import *


class User(DateBaseModel, AbstractUser):
    username = models.CharField(verbose_name="Username", max_length=50, unique=True)
    first_name = models.CharField(verbose_name="Firstname", max_length=50)
    last_name = models.CharField(verbose_name="Lastname", max_length=50)
    email = models.EmailField(verbose_name="Email", unique=True)
    phone_no = models.CharField(verbose_name="Phone no", max_length=15)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
