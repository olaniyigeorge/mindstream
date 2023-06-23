from django.urls import path

from . import views


urlpatterns = [
    path('', views.profile, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('mfa2', views.login, name='recovery_question'),
    path('logout', views.logout, name='logout')
]