from django.contrib import admin, messages
from .models import RecurringTask, Task, TaskList, Tag

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['title', 'deadline', 'slug', 'tags']
    readonly_fields = ['slug']
    list_display = ('title', 'deadline', 'priority', 'done', 'task_list')
    list_display_links = ('title', )
    filter_horizontal = ['tags']
    ordering = ['deadline', 'title']
    list_editable = ('deadline', 'done', )
    list_per_page = 10
    actions = ['set_done', 'set_undone']
    search_fields = ['title', 'task_list__title']
    list_filter = ['task_list__title', 'done']

    @admin.action(description='set tasks done')
    def set_done(self, request, queryset):
        count = queryset.update(done=True)
        if count == 1:
            message = "1 task was marked as done."
        else:
            message = f"{count} tasks were marked as done."
        self.message_user(request, message)

    @admin.action(description='set tasks undone')
    def set_undone(self, request, queryset):
        count = queryset.update(done=False)
        if count == 1:
            message = "1 task was marked as undone."
        else:
            message = f"{count} tasks were marked as undone."
        self.message_user(request, message, messages.WARNING)
 

@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_display_links = ('id', 'title')
    ordering = ['title']

admin.site.register(Tag)
admin.site.register(RecurringTask)

