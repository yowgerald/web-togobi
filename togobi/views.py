from togobi.serializers  import UserContentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

# Create your views here.
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def user_content_collection(request):
	if request.method == 'GET':
		users = User.objects.all()
		serializer = UserContentSerializer(users, many=True)
		return Response(serializer.data)

