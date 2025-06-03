from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name = "Task type"
        verbose_name_plural = "Task types"

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self) -> str:
        return f"{self.username} ({self.position})"
    
    def get_absolute_url(self):
        return reverse("main:worker-detail", args=[str(self.id)])


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="workers")

    class Meta:
        ordering = ["is_completed", "deadline", "name"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return f"{self.name}(type: {self.task_type}, deadline: {self.deadline}, priority: {self.priority}, is_completed: {self.is_completed})"
