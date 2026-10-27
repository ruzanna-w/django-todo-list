from django.forms import ModelForm 
from django import forms
from .models import Task
import datetime 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        labels = {
            'title': 'Task title',
            'description': 'Description',
            'deadline': 'Deadline',
            'priority': 'Priority',
            'done': 'Mark as completed',
            'task_list': 'Category',
            'tags': 'Tags'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task title',
                'class': 'form-control'
            }),
            'description': forms.TextInput(attrs={
                'placeholder': 'Enter task description',
                'class': 'form-control'
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'tag-checkbox'
            }),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']

        if deadline < datetime.date.today():
            raise ValidationError(_('Invalid date - deadline is in the past'))
        
        return deadline
    
class TaskStatusForm(ModelForm):
    class Meta:
        model = Task
        fields = ['done']
        widgets = {
            'done': forms.CheckboxInput(attrs={
                'class': 'task-status'
            }),
        }