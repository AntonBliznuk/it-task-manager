from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from main.models import TaskType, Position, Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_of_workers": Worker.objects.all().count(),
        "num_of_tasks": Task.objects.all().count(),
        "num_of_positions": Position.objects.all().count()
    }
    return render(request, "main/index.html", context=context)


class PositionListView(generic.ListView):
    model = Position


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("main:position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("main:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    template_name = "main/position_confirm_delete.html"
    success_url = reverse_lazy("main:position-list")


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "main/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("main:task-type-list")
    template_name = "main/task_type_form.html"


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("main:task-type-list")
    template_name = "main/task_type_form.html"


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    template_name = "main/task_type_confirm_delete.html"
    success_url = reverse_lazy("main:task-type-list")