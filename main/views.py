from django.shortcuts import get_object_or_404, redirect,render
from main.models import Experience, Project, Education
from main.forms import ProjectForm, ExperienceForm, EducationForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse



def show_main(request):
    context = {
        "name": "Keizora",
        "npm": "2506597510",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Undergraduate Information Systems student at University of Indonesia. "
            "Starting my second year and surprisingly still surviving (hopefully)."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    experiences = [experience.object for experience in experiences]

    context = {
        "name": "Keizora",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Keizora",
        "form": form,
        "form_title": "Tambah Experience",
        "submit_text": "Tambah Experience",
    }

    return render(request, "experience_form.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Keizora",
        "form": form,
        "form_title": "Edit Experience",
        "submit_text": "Simpan Perubahan",
    }

    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")

    return redirect("main:show_experience")


def get_experience_json(request):
    experiences = Experience.objects.all()

    experiences_json = serializers.serialize(
        "json",
        experiences
    )

    return HttpResponse(
        experiences_json,
        content_type="application/json"
    )

def show_education(request):
    json_response = get_education_json(request)

    education_list = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    education_list = [
        education.object
        for education in education_list
    ]

    context = {
        "name": "Keizora",
        "education_list": education_list,
    }

    return render(
        request,
        "education.html",
        context
    )


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Pendidikan berhasil ditambahkan!"
        )
        return redirect("main:show_education")

    context = {
        "name": "Keizora",
        "form": form,
        "form_title": "Tambah Pendidikan",
        "submit_text": "Tambah Pendidikan",
    }

    return render(
        request,
        "education_form.html",
        context
    )


def update_education(request, education_id):
    education = get_object_or_404(
        Education,
        pk=education_id
    )

    form = EducationForm(
        request.POST or None,
        instance=education
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Pendidikan berhasil diperbarui!"
        )
        return redirect("main:show_education")

    context = {
        "name": "Keizora",
        "form": form,
        "form_title": "Edit Pendidikan",
        "submit_text": "Simpan Perubahan",
    }

    return render(
        request,
        "education_form.html",
        context
    )


def delete_education(request, education_id):
    education = get_object_or_404(
        Education,
        pk=education_id
    )

    if request.method == "POST":
        education.delete()
        messages.success(
            request,
            "Pendidikan berhasil dihapus!"
        )

    return redirect("main:show_education")


def get_education_json(request):
    education_list = Education.objects.all()

    education_json = serializers.serialize(
        "json",
        education_list
    )

    return HttpResponse(
        education_json,
        content_type="application/json"
    )

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Keizora",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Keizora",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")