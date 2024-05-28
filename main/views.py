from django.shortcuts import render, get_object_or_404
from .models import Project, Tag


# Create your views here.

def home(request):
    return render(request, "home.html")


def projects(request):
    projects = Project.objects.all()
    tags = Tag.objects.all()

    return render(request, "projects.html", {"projects": projects, "tags": tags})


def tools(request):
    return render(request, "tools.html")
def contact(request):
    context = {'email': 'support@journeyinto.tech'}
    return render(request, 'contact.html', context)

def resume(request):
    return render(request, "resume.html")


def project(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, "project.html", {"project": project})
