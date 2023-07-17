from django.urls import path
from . import views

app_name = "journal"

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path("create", views.create_entry, name="create_entry"),
    path("search-archive", views.search_archive, name="search-archive"),
    path("day/<int:year>/<int:month>/<int:day>", views.day_view, name='day_view'),

    #path("delete/<int:entry_id>", views.delete, name="delete"),
    #path("archive/<str:filter_on>", views.archive, name='archive')
]