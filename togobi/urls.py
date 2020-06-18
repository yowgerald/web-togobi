from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^content/(?P<id>\d+)$', views.content_details, name='content_details'),
    url(r'^content/(?P<id>\d+)/join$', views.content_join, name='content_join'),
]