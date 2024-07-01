from account.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Payment(models.Model):
    amount = models.IntegerField(max_length=50_000_000)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
