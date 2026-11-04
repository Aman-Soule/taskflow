from django.conf import settings
from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField("nom", max_length=120)
    description = models.TextField(blank=True)
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name= "projects",
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.name
    
class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "À faire"
        DOING = "doing", "En cours"
        DONE = "done", "Terminée"
        
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    
    title = models.CharField("titre", max_length=200)
    
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TODO)
    
    due_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title