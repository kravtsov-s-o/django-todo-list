from django.contrib import admin

from todo_list.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "end_date", "is_completed", "owner", "created_at"]
    list_filter = ["is_completed", "owner"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]
