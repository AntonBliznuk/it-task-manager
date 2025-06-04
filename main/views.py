from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from main.models import Position, Task, TaskType, Worker
from main.forms import WorkerCreationForm, WorkerPositionUpdateForm, WorkerSearchForm


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_of_workers": Worker.objects.all().count(),
        "num_of_tasks": Task.objects.all().count(),
        "num_of_positions": Position.objects.all().count()
    }
    return render(request, "main/index.html", context=context)


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    queryset = Position.objects.prefetch_related("workers")
    paginate_by = 10


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("main:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("main:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "main/position_confirm_delete.html"
    success_url = reverse_lazy("main:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 10
    queryset = TaskType.objects.prefetch_related("tasks")
    template_name = "main/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("main:task-type-list")
    template_name = "main/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("main:task-type-list")
    template_name = "main/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "main/task_type_confirm_delete.html"
    success_url = reverse_lazy("main:task-type-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username_or_position_name = self.request.GET.get("username_or_position_name", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username_or_position_name": username_or_position_name}
        )
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Worker.objects.select_related("position").prefetch_related("tasks")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data["username_or_position_name"]
            return queryset.filter(
                Q(username__icontains=search_term) |
                Q(position__name__icontains=search_term)
                )
        return queryset


def worker_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    worker = get_object_or_404(Worker.objects.prefetch_related("tasks"), pk=pk)
    assigned_tasks = worker.tasks.all()
    assigned_tasks_count = assigned_tasks.count()
    completed_tasks_count = assigned_tasks.filter(is_completed=True).count()

    context = {
        "worker": worker,
        "assigned_tasks": assigned_tasks,
        "assigned_tasks_count": assigned_tasks_count,
        "completed_tasks_count": completed_tasks_count,
        "today": now(),
    }

    return render(request, "main/worker_detail.html", context=context)


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    success_url = reverse_lazy("main:worker-list")
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    success_url = reverse_lazy("main:worker-list")
    form_class = WorkerPositionUpdateForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("main:worker-list")
    template_name = "main/worker_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("main:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("main:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "main/task_confirm_delete.html"
    success_url = reverse_lazy("main:task-list")
