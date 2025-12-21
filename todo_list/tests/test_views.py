from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from todo_list.models import Task

User = get_user_model()


class TaskListViewTests(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="user1",
            password="password123"
        )
        self.user_2 = User.objects.create_user(
            username="user2",
            password="password123"
        )

        Task.objects.create(
            title="User 1 task",
            owner=self.user_1
        )
        Task.objects.create(
            title="User 2 task",
            owner=self.user_2
        )

    def test_user_sees_only_own_tasks(self):
        self.client.login(username="user1", password="password123")

        url = reverse("todo_list:task_list")
        response = self.client.get(url)

        tasks = response.context["tasks"]

        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks.first().title, "User 1 task")

    def test_task_filters(self):
        self.client.login(username="user1", password="password123")

        Task.objects.create(
            title="Completed task",
            owner=self.user_1,
            is_completed=True
        )

        cases = [
            ("active", 1, False),
            ("done", 1, True),
            ("all", 2, None),
        ]

        for status, expected_count, completed in cases:
            with self.subTest(status=status):
                url = reverse("todo_list:task_list") + f"?status={status}"
                response = self.client.get(url)

                tasks = response.context["tasks"]
                self.assertEqual(tasks.count(), expected_count)

                if completed is not None:
                    self.assertEqual(tasks.first().is_completed, completed)

    def test_bulk_delete_tasks(self):
        self.client.login(username="user1", password="password123")

        Task.objects.create(
            title="Task 1",
            owner=self.user_1
        )
        Task.objects.create(
            title="Task 2",
            owner=self.user_1
        )

        url = reverse("todo_list:task_delete_all")
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Task.objects.filter(owner=self.user_1).count(),
            0
        )

    def test_toggle_task_status(self):
        self.client.login(username="user1", password="password123")

        task = Task.objects.create(
            title="Test task",
            owner=self.user_1,
            is_completed=False
        )

        url = reverse("todo_list:task_change_status", args=[task.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_cannot_toggle_someone_task(self):

        self.client.login(username="user1", password="password123")

        someone_task = Task.objects.create(
            title="Other user's task",
            owner=self.user_2,
            is_completed=False
        )

        url = reverse("todo_list:task_change_status", args=[someone_task.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

        someone_task.refresh_from_db()
        self.assertFalse(someone_task.is_completed)