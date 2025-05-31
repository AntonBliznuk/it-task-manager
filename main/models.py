from django.contrib.auth.models import AbstractUser
from django.db import models


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
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self) -> str:
        return f"{self.username} ({self.position})"
