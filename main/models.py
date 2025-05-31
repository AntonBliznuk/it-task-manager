from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name = "Task type"
        verbose_name = "Task types"

    def __str__(self) -> str:
        return self.name
