from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    # username = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    national_code = models.CharField(max_length=10)

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f'{self.phone_number}'
