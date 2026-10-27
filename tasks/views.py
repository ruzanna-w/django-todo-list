from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task, TaskList, Tag
from .forms import TaskForm, TaskStatusForm


# Create your views here.
def home(request):
    return render(request, "tasks/home.html")

def task_list(request):
    all_tasks = Task.objects.all()
    return render(request, "tasks/all_tasks.html", {"all_tasks": all_tasks})

def task_category(request):
    if request.method == "POST":
        title = request.POST["title"]
        TaskList.objects.create(title=title)
        return redirect("tasks:task_category")
    
    task_category = TaskList.objects.all()
    return render(request, "tasks/task_category.html", {"task_category": task_category})

def tag_list(request):
    if request.method == "POST":
        title = request.POST["title"]
        Tag.objects.create(title=title)
        return redirect("tasks:tag")
        
    tag = Tag.objects.all()
    return render(request, "tasks/tag.html", {"tag": tag})

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("tasks:add_task")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {'form':form})


def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("tasks:tasks")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form, 'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("tasks:tasks")

    return render(request, "tasks/task_delete.html", {"task": task})

def change_status(request):
    if request.method == 'POST':
        task_id = request.POST.get("task")
        task = get_object_or_404(Task, id=task_id)

        form = TaskStatusForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
    
    return redirect("tasks:tasks")

def page_not_found(request, exception):
    return render(request, '404.html', status=404)