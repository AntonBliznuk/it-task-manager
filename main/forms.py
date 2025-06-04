from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import Worker, Task
from django.contrib.auth import get_user_model


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class WorkerPositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["username", "first_name", "last_name", "position"]


class WorkerSearchForm(forms.Form):
    username_or_position_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username or position..."})
    )


class TaskSearchForm(forms.Form):
    name_or_priority = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name or priority..."})
    )


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local"
        }),
        input_formats=["%Y-%m-%dT%H:%M"]
    )

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-select"
        }),
        required=False
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
            "is_completed"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }