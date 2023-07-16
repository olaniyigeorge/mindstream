from django.urls import path
from . import views

app_name = "journal"
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path("create", views.create_entry, name="create_entry"),
    path("day/<int:day>/<int:month>/<int:year>", views.day, name='day_view'),
    #path("delete/<int:entry_id>", views.delete, name="delete"),
    path("archive/<str:filter_on>", views.archive, name='archive')
]