from django.urls import path

from . import views
from . import apis

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:target_id>', views.prep_room, name='prep_room'),
    path('room/go/<str:room>', views.goto_room, name='goto_room'),

    path('room/message/add', apis.message_add),
    path('room/messages/<int:recepient>', apis.message_collection)
]