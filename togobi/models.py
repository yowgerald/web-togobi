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


class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    target_date = models.DateTimeField('target date', null=True)
    is_active = models.BooleanField(default=True)
    location = models.ForeignKey(
        'Location', on_delete=models.SET_NULL, null=True)
    creation_step = models.IntegerField(default=1)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)


class ContentFile(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, related_name='content_files')
    source = models.CharField(max_length=200, null=True)
    f_type = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=False)

class ContentJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    status = models.IntegerField()
    remarks = models.CharField(max_length=200, null=True)
    application_date = models.DateTimeField('date applied')
    accepted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='content_author')
    accepted_date = models.DateTimeField('date accepted', null=True)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    m_type = models.CharField(max_length=50, null=True)
    status = models.IntegerField()
    sent_date = models.DateTimeField('date sent', null=True)

class MessageReceiver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)

    
# TODO: add content_fb
# TODO: add content_sms
