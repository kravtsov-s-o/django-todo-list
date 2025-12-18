from django import forms

from todo_list.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {
            "title": forms.TextInput(attrs={'class': "form-control mb-3"}),
            "description": forms.Textarea(attrs={'class': "form-control mb-3", 'style': "height: 100px;"}),
            "end_date": forms.DateInput(attrs={'type': 'date', 'class': "form-control mb-3"}),
            "is_completed": forms.CheckboxInput(attrs={'class': "form-check-input mb-3"}),
        }
        fields = ["title", "description", "end_date", "is_completed"]
