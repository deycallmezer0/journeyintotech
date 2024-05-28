from django.shortcuts import render, get_object_or_404
from .models import Project, Tag, Tools

# Create your views here.

def home(request):
    return render(request, "home.html")


def projects(request):
    projects = Project.objects.all()
    tags = Tag.objects.all()

    return render(request, "projects.html", {"projects": projects, "tags": tags})


def tools(request):
    tools = Tools.objects.all()
    return render(request, "tools.html", {"tools": tools})

def contact(request):
    context = {'email': 'support@journeyinto.tech'}
    return render(request, 'contact.html', context)


def tools_list(request):
    tools = Tools.objects.all()
    return render(request, 'tools/tools_list.html', {'tools': tools})

def resume(request):
    return render(request, "resume.html")


def project(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, "project.html", {"project": project})
