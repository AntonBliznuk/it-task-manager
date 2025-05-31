from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import TaskType, Position, Worker


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
