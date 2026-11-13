from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task, TaskList, Tag, RecurringTask
from .forms import TaskForm, TaskStatusForm, TagForm, TaskListForm
from django.db.models import Count


# Create your views here.
def home(request):
    return render(request, "tasks/home.html")

def task_list(request):
    all_tasks = Task.objects.select_related("recurring_task").prefetch_related('tags')

    for task in all_tasks:
        task.status_form = TaskStatusForm(instance=task)
    
    return render(request, "tasks/all_tasks.html", {"all_tasks": all_tasks})

def task_category(request):
    if request.method == "POST":
        category_form = TaskListForm(request.POST)

        if category_form.is_valid():
            category_form.save()
            return redirect("tasks:task_category")
    else:
        category_form = TaskListForm()
    
    categories = TaskList.objects.annotate(
        task_count=Count("tasks")
        ).prefetch_related("tasks")
    return render(request, 
        "tasks/task_category.html", {
        "categories": categories, 
        "category_form": category_form
    })

def tag_list(request):
    if request.method == "POST":
        tag_form = TagForm(request.POST)

        if tag_form.is_valid():
            tag_form.save()
            return redirect("tasks:tag")

    else:
        tag_form = TagForm()
        
    tags = Tag.objects.all()
    selected_tags = request.GET.getlist("tags")
    tasks = Task.objects.filter(tags__id__in=selected_tags).distinct()
    tasks_count = tasks.count()

    return render(request, "tasks/tag.html", {
        "tag": tags,
        "tag_form": tag_form,
        "selected_tags": selected_tags,
        "selected_count": len(selected_tags),
        "tasks": tasks,
        "tasks_count": tasks_count,
    })

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            if form.cleaned_data["repeat"]:
                RecurringTask.objects.create(
                    task_ptr=task,
                    title=task.title,
                    slug=task.slug,
                    description=task.description,
                    deadline=task.deadline,
                    priority=task.priority,
                    done=task.done,
                    task_list=task.task_list,
                    periodicity_days=form.cleaned_data["periodicity_days"],
                )
            return redirect("tasks:tasks")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {'form': form})

def edit(request, task_slug):
    task = get_object_or_404(Task, slug=task_slug)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            if form.cleaned_data["repeat"]:
                RecurringTask.objects.update_or_create(
                    task_ptr=task,
                    defaults={
                        "periodicity_days": form.cleaned_data["periodicity_days"],
                    },
                )
            else:
                recurring_task = RecurringTask.objects.filter(pk=task.pk).first()
                if recurring_task:
                    recurring_task.delete(keep_parents=True)

            return redirect("tasks:tasks")
    else:
        recurring_task = RecurringTask.objects.filter(pk=task.pk).first()

        form = TaskForm(
            instance=task,
            initial={
                "repeat": recurring_task is not None,
                "periodicity_days": (
                    recurring_task.periodicity_days if recurring_task else None
                ),
            },
        )

    return render(request, "tasks/task_form.html", {"form": form, "task": task})


def delete_task(request, task_slug):
    task = get_object_or_404(Task, slug=task_slug)

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

def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    if request.method == 'POST':
        tag.delete()
        return redirect("tasks:tag")
    
    return render(request, "tasks/tag_delete.html", {"tag": tag})

def delete_category(request, task_list_id):
    task_category = get_object_or_404(TaskList, id=task_list_id)

    if request.method == 'POST':
        task_category.delete()
        return redirect("tasks:task_category")
    return render(request, "tasks/category_delete.html", {"task_category": task_category})    

def page_not_found(request, exception):
    return render(request, '404.html', status=404)