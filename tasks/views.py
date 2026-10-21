from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task, TaskList, Tag


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
        title = request.POST["title"].capitalize()
        description = request.POST["description"].capitalize()
        deadline = request.POST["deadline"]
        priority = request.POST["priority"]
        category_id = request.POST.get("category")
        tag_ids = request.POST.getlist("tags")

        task = Task.objects.create(
            title = title,
            description = description,
            deadline = deadline,
            priority = priority,
            task_list_id = category_id or None,
        )

        task.tags.set(tag_ids)

        return redirect("tasks:add_task")
        
    tag_list = Tag.objects.all()
    task_list = TaskList.objects.all()

    return render(request, "tasks/task_form.html", {
        "tag_list": tag_list,
        "task_list": task_list,
        })

def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        deadline = request.POST["deadline"]
        priority = request.POST["priority"]
        category_id = request.POST.get("category")
        tag_ids = request.POST.getlist("tags")

        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.task_list_id = category_id or None

        task.save()
        task.tags.set(tag_ids)

        return redirect("tasks:tasks")

    tag_list = Tag.objects.all()
    task_list = TaskList.objects.all()

    return render(request, "tasks/task_form.html", {
        "task": task,
        "tag_list": tag_list,
        "task_list": task_list,
    })

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("tasks:tasks")

    return render(request, "tasks/task_delete.html", {"task": task})

def change_status(request):
    if request.method == 'POST':
        task_id = request.POST["task"]
        task = Task.objects.get(id=task_id)
        if task.done:
            task.done = False
            task.save()
        else:
            task.done = True
            task.save()
    
        return redirect("tasks:tasks")

