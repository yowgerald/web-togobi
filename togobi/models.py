from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# TODO: rethink if there is an event with no location
class Location(models.Model):
    name = models.CharField(max_length=200)
    coordinates  = models.CharField(max_length=200)

class Plan(models.Model):
    name = models.CharField(max_length=200)
    discount = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    is_active = models.BooleanField(default=True)

class Bank(models.Model):
    name = models.CharField(max_length=200)

class CardType(models.Model):
    name = models.CharField(max_length=200)

class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField('date updated')

class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=200)
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, null=True)
    c_type = models.ForeignKey('CardType', on_delete=models.SET_NULL, null=True)
    expiration_date = models.DateTimeField('expiry date')
    is_active = models.BooleanField(default=False)

class FileType(models.Model):
    name = models.CharField(max_length=200)

class Content(models.Model):
    user = models.ForeignKey(User, related_name='contents', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')

class ContentFile(models.Model):
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    f_type = models.ForeignKey('FileType', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)

# TODO: add content_fb
# TODO: add content_sms