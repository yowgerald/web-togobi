from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate')
]