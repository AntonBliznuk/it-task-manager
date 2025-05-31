from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import TaskType, Position, Worker, Task


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (
        (
            ("Additional Info"), {"fields": ("position", )}
        ), 
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            ("Additional Info"), {"fields": ("first_name", "last_name", "position", )}
        ),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "deadline", "is_completed", "priority", "task_type"]
    list_filter = ["task_type", "priority"]
    search_fields = ["name", "description"]
