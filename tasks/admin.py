from django.contrib import admin
from .models import Task, TaskList, Tag

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(Tag)
