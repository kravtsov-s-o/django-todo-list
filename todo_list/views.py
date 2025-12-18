from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from todo_list.forms import TaskForm
from todo_list.models import Task


# Create your views here.
class MainView(View):
    def get(self, request):
        return redirect('todo_list:task_list')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo_list/index.html"
    context_object_name = "tasks"
    paginate_by = 20

    def get_queryset(self):
        tasks = Task.objects.filter(owner=self.request.user)
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "today": timezone.localdate(),
        })
        return context


class TaskAddView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_list/create.html"

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "todo_list:task_list"
        )


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_list/create.html"

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "todo_list:task_list"
        )


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_success_url(self):
        success_url = self.request.META.get("HTTP_REFERER", "/")

        return success_url


class TaskToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user)

        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed"])

        return redirect("todo_list:task_list")
