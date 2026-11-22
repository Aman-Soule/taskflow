from django import forms
from .models import Project, Task


class StyledFormMixin:
    """Ajoute la classe CSS 'form-control' à tous les champs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]


class TaskForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["project", "title", "status", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:  # on ne propose que les projets de l'utilisateur
            self.fields["project"].queryset = Project.objects.filter(owner=user)