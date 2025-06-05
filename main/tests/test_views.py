from django.test import TestCase
from django.urls import reverse

from main.models import Worker, Task, Position, TaskType


class PublicViewsTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        self.assertEqual(
            response.context.get("num_of_workers"),
            Worker.objects.all().count()
        )
        self.assertEqual(
            response.context.get("num_of_tasks"),
            Task.objects.all().count()
        )
        self.assertEqual(
            response.context.get("num_of_positions"),
            Position.objects.all().count()
        )

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")