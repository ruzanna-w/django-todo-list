from django.db import models

# Create your models here.
class TaskList(models.Model):
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class Tag(models.Model):
    title = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.title}"

class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    deadline = models.DateField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    done = models.BooleanField(default=False)
    task_list = models.ForeignKey(
        TaskList, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.title}"


class RecurringTask(Task):
    periodicity_hours = models.PositiveIntegerField(
        help_text="Интервал повторения задачи в часах."
    )
