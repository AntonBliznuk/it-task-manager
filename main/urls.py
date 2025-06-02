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
]

app_name = "main"
