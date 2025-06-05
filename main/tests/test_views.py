from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from main.models import Worker, Task, Position, TaskType


class PublicViewsTest(TestCase):
    def test_index_view_public(self):
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

    def test_login_view_public(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_get_worker_create_view_public(self):
        response = self.client.get(reverse("main:worker-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/worker_form.html")

    def test_post_worker_create_view_valid_data_public(self):
        form_data = {
            "username": "test_worker",
            "password1": "Strongpassword123%",
            "password2": "Strongpassword123%",
        }
        response = self.client.post(reverse("main:worker-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Worker.objects.filter(username="test_worker").exists())

    def test_post_worker_create_view_invalid_data_public(self):
        form_data = {
            "username": "wrong",
            "password1": "123",
            "password2": "123",
        }
        response = self.client.post(reverse("main:worker-create"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Worker.objects.filter(username="wrong").exists())


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

    def test_position_list_view(self):
        response = self.client.get(reverse("main:position-list"))
        self.assertEqual(response.status_code, 200)

    def test_position_create_view(self):
        response = self.client.get(reverse("main:position-create"))
        self.assertEqual(response.status_code, 200)

    def test_position_update_view(self):
        pos = Position.objects.create(name="Manager")
        response = self.client.get(reverse("main:position-update", args=[pos.id]))
        self.assertEqual(response.status_code, 200)

    def test_position_delete_view(self):
        pos = Position.objects.create(name="Developer")
        response = self.client.get(reverse("main:position-delete", args=[pos.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_type_list_view(self):
        response = self.client.get(reverse("main:task-type-list"))
        self.assertEqual(response.status_code, 200)

    def test_task_type_create_view(self):
        response = self.client.get(reverse("main:task-type-create"))
        self.assertEqual(response.status_code, 200)

    def test_task_type_update_view(self):
        task_type = TaskType.objects.create(name="Bug")
        response = self.client.get(reverse("main:task-type-update", args=[task_type.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_type_delete_view(self):
        task_type = TaskType.objects.create(name="Feature")
        response = self.client.get(reverse("main:task-type-delete", args=[task_type.id]))
        self.assertEqual(response.status_code, 200)

    def test_worker_list_view(self):
        response = self.client.get(reverse("main:worker-list"))
        self.assertEqual(response.status_code, 200)

    def test_worker_detail_view(self):
        position = Position.objects.create(name="Tester")
        worker = Worker.objects.create_user(username="worker1", password="pass", position=position)
        response = self.client.get(reverse("main:worker-detail", args=[worker.id]))
        self.assertEqual(response.status_code, 200)

    def test_worker_update_view(self):
        position = Position.objects.create(name="Leader")
        worker = Worker.objects.create_user(username="worker2", password="pass", position=position)
        response = self.client.get(reverse("main:worker-update", args=[worker.id]))
        self.assertEqual(response.status_code, 200)

    def test_worker_delete_view(self):
        position = Position.objects.create(name="Leader")
        worker = Worker.objects.create_user(username="worker3", password="pass", position=position)
        response = self.client.get(reverse("main:worker-delete", args=[worker.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view(self):
        response = self.client.get(reverse("main:task-list"))
        self.assertEqual(response.status_code, 200)

    def test_task_create_view(self):
        response = self.client.get(reverse("main:task-create"))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view(self):
        task_type = TaskType.objects.create(name="Fix")
        task = Task.objects.create(name="Fix bug", deadline="2025-12-12", priority="High", task_type=task_type)
        response = self.client.get(reverse("main:task-detail", args=[task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_update_view(self):
        task_type = TaskType.objects.create(name="Build")
        task = Task.objects.create(name="Build system", deadline="2025-12-12", priority="Medium", task_type=task_type)
        response = self.client.get(reverse("main:task-update", args=[task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view(self):
        task_type = TaskType.objects.create(name="Cleanup")
        task = Task.objects.create(name="Clean code", deadline="2025-12-12", priority="Low", task_type=task_type)
        response = self.client.get(reverse("main:task-delete", args=[task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_complete_view(self):
        task_type = TaskType.objects.create(name="Check")
        task = Task.objects.create(name="Check logs", deadline="2025-12-12", priority="High", task_type=task_type)
        response = self.client.post(reverse("main:task-complete", args=[task.id]))
        self.assertRedirects(response, reverse("main:task-detail", args=[task.id]))

    def test_task_assign_me_view(self):
        task_type = TaskType.objects.create(name="Write")
        task = Task.objects.create(name="Write report", deadline="2025-12-12", priority="High", task_type=task_type)
        response = self.client.post(reverse("main:task-assign-me", args=[task.id]))
        self.assertRedirects(response, reverse("main:task-detail", args=[task.id]))

    def test_task_unassign_worker_view(self):
        task_type = TaskType.objects.create(name="Unassign")
        task = Task.objects.create(name="Unassign task", deadline="2025-12-12", priority="Low", task_type=task_type)
        task.assignees.add(self.user)
        response = self.client.post(reverse("main:task-unassign-worker", args=[task.id, self.user.id]))
        self.assertRedirects(response, reverse("main:task-detail", args=[task.id]))