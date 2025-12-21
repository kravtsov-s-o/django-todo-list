from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from todo_list.models import Task

User = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test",
            email="1@1.loc",
            password="password12345"
        )

    def test_end_date_cannot_be_in_the_past(self):
        past_date = timezone.localdate() - timedelta(days=1)

        task = Task(
            title="Test Task",
            description="Test description",
            owner=self.user,
            end_date=past_date
        )

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_valid_end_date(self):
        future_date = timezone.localdate() + timedelta(days=1)

        task = Task(
            title="Valid Task",
            description="Test description",
            owner=self.user,
            end_date=future_date
        )

        try:
            task.full_clean()
        except ValidationError:
            self.fail("Task with future end_date should be valid")

    def test_title_max_length(self):
        future_date = timezone.localdate() + timedelta(days=1)
        title = "A" * 31

        task = Task(
            title=title,
            description="Test description",
            owner=self.user,
            end_date=future_date
        )

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_title_max_length_valid(self):
        future_date = timezone.localdate() + timedelta(days=1)
        title = "A" * 30

        task = Task(
            title=title,
            description="Test description",
            owner=self.user,
            end_date=future_date
        )

        try:
            task.full_clean()
        except ValidationError:
            self.fail("Title can be longer 30 characters")
