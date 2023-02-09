from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    is_active = models.BooleanField(default=True)

class Promo(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    availability_date = models.DateTimeField('availability date')
    expiration_date = models.DateTimeField('expiry date')

class UserDiscount(models.Model):
    discount = models.DecimalField(max_digits=12, decimal_places=4),
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    promo = models.ForeignKey(Promo, on_delete=models.DO_NOTHING, null=True)
    is_active = models.BooleanField(default=True)

class Bank(models.Model):
    name = models.CharField(max_length=200)

class CardType(models.Model):
    name = models.CharField(max_length=200)

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=200)
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, null=True)
    c_type = models.ForeignKey('CardType', on_delete=models.SET_NULL, null=True)
    expiration_date = models.DateTimeField('expiry date')
    is_active = models.BooleanField(default=False)
