from django.urls import path

from todo_list.views import MainView, TaskListView, TaskAddView, TaskUpdateView, TaskDeleteView, TaskToggleCompleteView, \
    TaskBulkDeleteView

app_name = "todo_list"

urlpatterns = [
    path('', MainView.as_view()),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskAddView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/delete-all/', TaskBulkDeleteView.as_view(), name='task_delete_all'),
    path('tasks/<int:pk>/change-status/', TaskToggleCompleteView.as_view(), name='task_change_status'),
]