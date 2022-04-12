from rest_framework import serializers
from chats.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'text',
            'recepient',
            'sender',
            'created_at',
        )