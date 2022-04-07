from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserChatSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_chat_setting')
    availability = models.CharField(max_length=200, default='allow all') # [allow all, only attendees, deny all]

class RoomGroup(models.Model):
    name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)

class RoomGroupUser(models.Model):
    room_group = models.ForeignKey(RoomGroup, on_delete=models.CASCADE, null=True, related_name='room_group_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=200, default='allowed') # [allowed, blocked, reported, limited features?]
    created_at = models.DateTimeField('date created', auto_now_add=True)

# TODO: need to recheck models below
class Message(models.Model):
    text = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    recepient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='recepient')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender')
    created_at = models.DateTimeField('date created', auto_now_add=True)

class MessageFile(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, related_name='message_files')
    name = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200, null=True)
    f_type = models.CharField(max_length=50, null=True)