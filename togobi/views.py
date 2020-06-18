from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from togobi.models import Content
from togobi.serializers  import UserContentSerializer

# Create your views here.
def content_details(request, id):
	if request.method == 'GET':
		content = Content.objects.get(id=id)
	return render(request, 'content_details.html', {'content': content})

def content_join(request, id):
	return render(request, 'content_join.html', {});

# API
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def user_content_collection(request):
	if request.method == 'GET':
		users = User.objects.all()
		serializer = UserContentSerializer(users, many=True)
		return Response(serializer.data)

