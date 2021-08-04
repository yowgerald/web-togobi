from django.urls import path

from . import views


urlpatterns = [
    path('', views.content_list, name='home'),
    path('content/<int:id>', views.content_detail, name='content_detail'),
    path('content/add', views.content_add, name='content_add'),
    path('content/<int:id>/join', views.content_join, name='content_join'),
    path('manage/contents', views.own_contents, name='own_contents'),
    path('manage/content/<int:id>/edit', views.own_content_edit, name='own_content_edit'),
    path('manage/content/<int:id>/details', views.own_content_details, name='own_content_details'),
    path('manage/content/<int:id>/delete', views.own_content_delete, name='own_content_delete'),
    path('notifs/tab', views.notifs, name='notifs'),
    
    path('form/content', views.form_content),    
    
    path('contents', views.content_collection),
    path('contents/today', views.contents_today),
    path('contents/top', views.contents_top),
    path('contents/<int:id>/content_files', views.content_file_collection),
    path('contents/<int:id>/content_file/upload', views.contentfile_upload),
    path('content_file/<int:id>/delete', views.content_file_delete),

    path('location/suggestions', views.location_suggestions),
]
