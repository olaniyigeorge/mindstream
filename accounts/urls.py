from django.urls import path

from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('setmfa', views.setmfa, name='setmfa'),
    path('login', views.login_view, name='login_view'), # Only redirects to the first level of the mfa view
    path('mfa/<int:level>', views.mfa, name='mfa')    
    
    # path('login', views.login, name='login'),
    # path('editprofile', views.editprofile, name='editprofile'),
    # path('mfa2', views.login, name='recovery_question'),
    # path('logout', views.logout, name='logout')
]