from django import forms

from todo_list.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "end_date", "is_completed"]
        widgets = {
            "end_date": forms.DateInput(attrs={'type': 'date'})
        }
