from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from chats.models import Message, RoomGroup, RoomGroupUser
from django.contrib.auth.models import User
from datetime import datetime
import random
import string

# Create your views here.

@login_required
def index(request):
    return render(request, 'chats/index.html')

def create_unique_room():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    disallowed_characters = "/,: "
    for character in disallowed_characters:
        date_time = date_time.replace(character, "")

    lower_alpha = string.ascii_lowercase
    upper_alpha = string.ascii_uppercase
    digits = string.digits

    chars = date_time + lower_alpha + upper_alpha + digits

    result = ''.join((random.choice(chars)) for x in range(20))
    room_group_name = date_time + result

    return room_group_name

def rg_user_add(user, room_group):
    room_group_user = RoomGroupUser.objects.create(
        user=user,
        room_group=room_group
    )
    room_group_user.save()

@login_required
def prep_room(request, target_id):
    target_user = get_object_or_404(User.objects.select_related(), pk=target_id)

    room_group = RoomGroup.objects.select_related().filter(
        room_group_users__user=target_user,
    ).first()

    if room_group is None:
        # check if the user is available for direct chatting
        get_object_or_404(User.objects.select_related().exclude(user_chat_setting__availability='deny all'), pk=target_id)

        room_group_name = create_unique_room()

        room_group = RoomGroup.objects.create(
            name=room_group_name
        )
        room_group.save()

        # add current user to room group users
        rg_user_add(request.user, room_group)

        # add the target user to room group users
        rg_user_add(target_user, room_group)
    else:
        room_group_name = room_group.name

    return redirect('/chat/room/go/' + room_group_name)
    


@login_required
def goto_room(request, room):
    room_group = get_object_or_404(RoomGroup.objects.select_related(),
        name=room,
        room_group_users__user=request.user,
        room_group_users__status='allowed'
    )

    return render(request, 'chats/room.html', {
        'room_group_name': room
    })