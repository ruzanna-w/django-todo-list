from django import forms
from .models import Task, TaskList, Tag
import datetime 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    repeat = forms.BooleanField(
        required=False, 
        label = "Repeat task",
        widget = forms.CheckboxInput(attrs={
            "class": "repeat-task-toggle",
        }))
    
    periodicity_days = forms.IntegerField(
        min_value=1,
        required=False,
        label="Repeat every (days)"
    )
    task_list = forms.ModelChoiceField(
        queryset=TaskList.objects.all(),
        empty_label="category isn't selected",
        required=False)
    
    priority = forms.ChoiceField(
        choices=Task.Priority.choices,
        initial=Task.Priority.MEDIUM,
        widget=forms.RadioSelect,
        required=False,
    )

    tags = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        )

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'priority', 'task_list', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task title',
                'class': 'form-control',
                'max_length': 50,
            }),
            'description': forms.TextInput(attrs={
                'placeholder': 'Enter task description',
                'class': 'form-control'
            }),
            'deadline': forms.DateInput(attrs={
                "type": "date",
                "format" : "%d-%m-%Y"
            }),

        }
    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('repeat') and not cleaned_data.get("periodicity_days"):
            self.add_error("periodicity_days", "Enter the repeat interval.")
        
        return cleaned_data
    
    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']

        if deadline < datetime.date.today():
            raise ValidationError(_('Invalid date - deadline is in the past'))
        
        return deadline
    
class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['done']
        widgets = {
            'done': forms.CheckboxInput(attrs={
                'class': 'task-status',
                'onchange': 'this.form.submit()',
            }),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if Tag.objects.filter(title__iexact=title).exists():
            raise ValidationError(_('This tag already exists'))
        return title
    
class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['title']
    
    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if TaskList.objects.filter(title__iexact=title).exists():
            raise ValidationError(_('This category already exists'))
        return title