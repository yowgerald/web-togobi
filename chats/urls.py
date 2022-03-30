from django.urls import path

from . import views

urlpatterns = [
    path('message', views.message_add, name='message_add'),
]