from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, RedirectView

from todo_list._mixins import TitleContextMixin
from todo_list.forms import TaskForm
from todo_list.models import Task


# Create your views here.
class MainView(RedirectView):
    pattern_name = 'todo_list:task_list'

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy("login")
        return super().get_redirect_url(*args, **kwargs)


class TaskListView(LoginRequiredMixin, TitleContextMixin, ListView):
    FILTER_ACTIVE = 'active'
    FILTER_DONE = 'done'
    FILTER_ALL = 'all'

    title = "Task List"
    model = Task
    template_name = "todo_list/index.html"
    context_object_name = "tasks"
    paginate_by = 20

    filters = (FILTER_ACTIVE, FILTER_DONE, FILTER_ALL)

    def get_queryset(self):
        tasks = Task.objects.filter(owner=self.request.user)

        self.filter_active = self.request.GET.get("status") or self.FILTER_ACTIVE

        if self.filter_active == self.FILTER_ACTIVE:
            return tasks.filter(is_completed=False)
        elif self.filter_active == self.FILTER_DONE:
            return tasks.filter(is_completed=True)

        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "today": timezone.localdate(),
            "filters": self.filters,
            "filter_active": self.filter_active,
        })
        return context


class TaskAddView(LoginRequiredMixin, TitleContextMixin, CreateView):
    title = "Create Task"
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


class TaskUpdateView(LoginRequiredMixin, TitleContextMixin, UpdateView):
    title = "Update Task"
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

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def get_success_url(self):
        success_url = self.request.META.get("HTTP_REFERER", "/")

        return success_url


class TaskBulkDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])

    def post(self, request):
        Task.objects.filter(owner=request.user).delete()
        return redirect("todo_list:task_list")


class TaskToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user)

        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed"])

        return redirect("todo_list:task_list")
