from django.db import models

from todo_list.utils import validate_future_date


# Create your models here.
class Task(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Owner")
    title = models.CharField(max_length=30, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    is_completed = models.BooleanField(default=False, verbose_name="Completed")
    end_date = models.DateField(blank=True, null=True,
                                    validators=[validate_future_date], verbose_name="End Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]