from django.db import models
from django.utils.text import slugify

def translit_to_eng(s: str) -> str:
    d = { 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 
        'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    return ''.join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

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
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
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

    class Meta: 
        ordering = ["deadline"]

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        
        base_slug = slugify(translit_to_eng(self.title)) or "task"
        slug = base_slug
        number = 2
        
        while Task.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{number}"
            number += 1
        
        self.slug = slug

        super().save(*args, **kwargs)

class RecurringTask(Task):
    task_ptr = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        parent_link = True,
        primary_key = True,
        related_name="recurring_task")
    
    periodicity_days = models.PositiveIntegerField(
        help_text="Repeat interval in days."
    )
