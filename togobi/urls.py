from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.content_list, name='home'),
    url(r'^content/detail', views.content_details, name='content_details'),
    url(r'^content/add', views.content_add, name='content_add'),
    url(r'^content/join', views.content_join, name='content_join'),
    url(r'^content/bookmark', views.content_bookmark, name='content_bookmark'),
]
