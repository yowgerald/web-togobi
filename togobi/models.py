from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# TODO: rethink if there is an event with no location


class Location(models.Model):
    name = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=200)


class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(
        'Location', on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(
        'payments.Plan', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField('date updated')


class FileType(models.Model):
    name = models.CharField(max_length=200)


class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    target_date = models.DateTimeField('target date', null=True)
    is_active = models.BooleanField(default=False)
    location = models.ForeignKey(
        'Location', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)


class ContentFile(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    source = models.CharField(max_length=200, null=True)
    f_type = models.ForeignKey(
        'FileType', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)

class ContentBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

class ContentJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200)
    application_date = models.DateTimeField('date applied')
    accepted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='content_author')
    accepted_date = models.DateTimeField('date accepted', null=True)
    
# TODO: add content_fb
# TODO: add content_sms
