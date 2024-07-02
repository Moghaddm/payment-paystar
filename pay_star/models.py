from account.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Payment(models.Model):
    amount = models.IntegerField(max_length=50_000_000)
    datetime = models.DateTimeField(auto_now_add=True)
    ref_num = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_successful = models.BooleanField()

    # payments = models.Manager()

# class PaymentManager(models.Model):
