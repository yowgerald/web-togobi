from chats.models import Message
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chats.serializers import MessageSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

@api_view(['POST'])
def message_add(request):
    sender = get_object_or_404(User, pk=request.POST.get('sender'))
    recepient = get_object_or_404(User, pk=request.POST.get('recepient'))
    
    message = Message()
    message.sender = sender # may need changing to logged user ?
    message.recepient = recepient
    message.text = request.POST.get('message')
    message.save()

    return JsonResponse(request.POST)

@api_view(['GET'])
def message_collection(request, recepient):
    user = get_object_or_404(User, pk=1) # must not be static
    recepient = get_object_or_404(User, pk=recepient)

    messages = Message.objects.filter(recepient=recepient, sender=user)
    serializer = MessageSerializer(messages, many=True)

    return Response({
        'result': serializer.data
    })