from rest_framework import serializers
from django.contrib.auth.models import User
from togobi.models import Content


class ContentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Content
        fields = (
            'id',
            'title',
            'description',
            'tags',
            'target_date',
            'username'
        )
