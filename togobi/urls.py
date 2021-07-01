from django.urls import path

from . import views


urlpatterns = [
    path('', views.content_list, name='home'),
    path('content/add', views.content_add, name='content_add'),
    path('content/<int:id>/details', views.content_details, name='content_details'),
    path('content/<int:id>/join', views.content_join, name='content_join'),
    path('manage/contents', views.own_contents, name='own_contents'),
    path('manage/content/<int:id>/edit', views.own_content_edit, name='own_content_edit'),
    path('manage/content/<int:id>/details', views.own_content_details, name='own_content_details'),
    path('manage/content/<int:id>/delete', views.own_content_delete, name='own_content_delete'),
    path('notifs/tab', views.notifs, name='notifs')
]
