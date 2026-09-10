from django.urls import path 
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index),
    path("create/", views.create_list),
    path("tag/", views.get_tag),
]