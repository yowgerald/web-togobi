from rest_framework import serializers
from togobi.models import Content, ContentFile


class ContentFileSerializer(serializers.ModelSerializer):
    signed_url = serializers.CharField(read_only=True)
    class Meta:
        model = ContentFile
        fields = (
            'id',
            'source',
            'f_type',
            'signed_url'
        )

class ContentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    content_files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Content
        fields = (
            'id',
            'title',
            'description',
            'tags',
            'target_date',
            'username',
            'content_files',
        )
