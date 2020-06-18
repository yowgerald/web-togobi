from rest_framework import serializers
from django.contrib.auth.models import User
from togobi.models import Content

class ContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Content
		fields = (
			'id',
			'title',
			'description',
			'tags',
			'target_date'
			)

class UserContentSerializer(serializers.ModelSerializer):
	contents = ContentSerializer(many=True)
	class Meta:
		model = User
		fields = (
			'username',
			'contents',
			)