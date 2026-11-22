from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import TaskForm
from .models import Project, Task
# Create your views here.

def home(request):
    return render(request, "tasks/home.html", {"active_menu": "dashboard"})




class UserTaskQuerysetMixin(LoginRequiredMixin):
    """Limite toutes les vues aux tâches des projets de l'utilisateur connecté."""
    def get_queryset(self):
        return (Task.objects
                .filter(project__owner=self.request.user)
                .select_related("project")
                .order_by("-created_at"))


class TaskFormMixin:
    """Envoie l'utilisateur au formulaire pour filtrer la liste des projets."""
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskListView(UserTaskQuerysetMixin, ListView):
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        status = self.request.GET.get("status")
        project = self.request.GET.get("project")
        if q:
            qs = qs.filter(title__icontains=q)
        if status:
            qs = qs.filter(status=status)
        if project:
            qs = qs.filter(project_id=project)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_menu"] = "tasks"
        ctx["status_choices"] = Task.Status.choices
        ctx["projects"] = Project.objects.filter(owner=self.request.user)
        return ctx


class TaskDetailView(UserTaskQuerysetMixin, DetailView):
    template_name = "tasks/task_detail.html"
    extra_context = {"active_menu": "tasks"}


class TaskCreateView(UserTaskQuerysetMixin, TaskFormMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")
    success_message = "Tâche créée."
    extra_context = {"active_menu": "tasks"}


class TaskUpdateView(UserTaskQuerysetMixin, TaskFormMixin, SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")
    success_message = "Tâche modifiée."
    extra_context = {"active_menu": "tasks"}


class TaskDeleteView(UserTaskQuerysetMixin, DeleteView):
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")

