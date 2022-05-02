from django.urls import path

from . import views
from . import apis


urlpatterns = [
    path('', views.content_list, name='home'),
    path('content/add', views.content_add, name='content_add'),
    path('content/<int:id>/join', views.content_join, name='content_join'),
    path('manage/contents', views.own_contents, name='own_contents'),
    path('manage/content/<int:id>/edit', views.own_content_edit, name='own_content_edit'),
    path('manage/content/<int:id>/delete', views.own_content_delete, name='own_content_delete'),
    path('manage/content/<int:id>/attendees', views.attendees_list, name='own_content_attendees'),
    path('manage/content/<int:id>/attendees/<int:attendee_id>/edit', views.attendee_edit, name='own_content_attendee_edit'),
    
    path('content/<int:id>', apis.content_detail, name='content_detail'),
    path('contents', apis.content_collection),
    path('contents/today', apis.contents_today),
    path('contents/top', apis.contents_top),
    path('contents/<int:id>/content_files', apis.content_file_collection),
    path('contents/<int:id>/content_file/upload', apis.contentfile_upload),
    path('content_file/<int:id>/delete', apis.content_file_delete),
]
