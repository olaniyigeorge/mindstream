from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('setmfa', views.setmfa, name='setmfa'),
    path('login', views.login_view, name='login_view'), # Only redirects to the first level of the mfa view
    path('mfa/<int:level>', views.mfa, name='mfa'),
    path('logout', views.logout_view, name='logout_view')
    
    # path('editprofile', views.editprofile, name='editprofile'),
    # path('mfa2', views.login, name='recovery_question'),
    # 
]