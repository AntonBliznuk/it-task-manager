from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="index"),

    path("positions/", views.PositionListView.as_view(), name="position-list"),
    path("positions/create/", views.PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", views.PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", views.PositionDeleteView.as_view(), name="position-delete"),

    path("task-types/", views.TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", views.TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", views.TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", views.TaskTypeDeleteView.as_view(), name="task-type-delete"),

    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/detail/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", views.WorkerDeleteView.as_view(), name="worker-delete"),

]

app_name = "main"
