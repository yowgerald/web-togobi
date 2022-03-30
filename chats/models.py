from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dialogue(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user2')
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

class Message(models.Model):
    text = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    recepient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='recepient')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender')
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

class MessageFile(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, related_name='message_files')
    name = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200, null=True)
    f_type = models.CharField(max_length=50, null=True)