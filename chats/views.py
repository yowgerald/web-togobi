from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'chats/index.html')

def room(request, room_name):
    return render(request, 'chats/room.html', {
        'room_name': room_name
    })