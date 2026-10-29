from django.urls import path 
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.task_list, name="tasks"),
    path("task_category/", views.task_category, name="task_category"),
    path("tag/", views.tag_list, name="tag"),
    path("form/", views.add_task, name='add_task'),
    path("<int:task_id>/edit/", views.edit, name="edit"),
    path("<int:task_id>/task_delete/", views.delete_task, name="task_delete"),
    path("task_status/", views.change_status, name="task_status"),
    path("<int:tag_id>/tag_delete/", views.delete_tag, name="delete_tag")
]

