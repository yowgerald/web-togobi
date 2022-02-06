from rest_framework import serializers
from togobi.models import Content, ContentFile, ContentJoin


class ContentFileSerializer(serializers.ModelSerializer):
    signed_url = serializers.CharField(read_only=True)
    class Meta:
        model = ContentFile
        fields = (
            'id',
            'name',
            'source',
            'f_type',
            'signed_url'
        )

class ContentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    content_files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    total_attendees = serializers.IntegerField(min_value=0, default=0)
    target_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
    class Meta:
        model = Content
        fields = (
            'id',
            'title',
            'description',
            'tags',
            'target_date',
            'is_active',
            'username',
            'content_files',
            'total_attendees',
        )

class ContentTopSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='content.id', read_only=True)
    title = serializers.CharField(source='content.title', read_only=True)
    class Meta:
        model = ContentJoin
        fields = (
            'id',
            'title'
        )
