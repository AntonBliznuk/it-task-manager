from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from main.models import TaskType, Position, Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_of_workers": Worker.objects.all().count(),
        "num_of_tasks": Task.objects.all().count(),
        "num_of_positions": Position.objects.all().count()
    }
    return render(request, "main/index.html", context=context)
