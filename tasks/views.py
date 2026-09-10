from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Task, TaskList, Tag


# Create your views here.
def index(request):
    task_list = Task.objects.all()
    return render(request, "tasks/index.html", {"task_list": task_list})

def create_list(request):
    task = TaskList.objects.all()
    return render(request, "tasks/index.html", {"task": task})

def get_tag(request):
    tag = Tag.objects.all()
    return render(request, "tasks/index.html", {"tag": tag})