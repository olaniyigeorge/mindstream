from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path("create", views.create_entry, name="create_entry"),
    path("delete/<int:entry_id>", views.delete, name="delete"),
    path("<int:day>/<int:month>/<int:year>", views.day, name='day_view'),
    path("archive/<str:filter_on>", views.archive, name='archive')
]