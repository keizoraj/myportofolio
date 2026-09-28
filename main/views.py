from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect,render
from main.models import Experience, Project, Education
from main.forms import ProjectForm, ExperienceForm, EducationForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Keizora",
        "npm": "2506597510",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Undergraduate Information Systems student at University of Indonesia. "
            "Starting my second year and surprisingly still surviving (hopefully)."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Keizora",
        "experience_list": Experience.objects.all(),
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)    

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not can_edit(request.user):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

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
    education_list = Education.objects.all()

    context = {
        "name": "Keizora",
        "education_list": education_list,
        "is_editor": is_editor(request.user),
    }

    return render(
        request,
        "education.html",
        context
    )

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url="/login/")
def update_education(request, education_id):
    if not can_edit(request.user):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not can_edit(request.user):
        raise PermissionDenied

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
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(
            title__icontains=title_query
        )

    context = {
        "name": "Keizora",
        "project_list": projects,
        "title_query": title_query,
        "is_editor": is_editor(request.user),
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

    projects_json = serializers.serialize(
        "json",
        projects,
        fields=(
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ),
    )
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def update_project(request, project_id):
    if not can_edit(request.user):
        raise PermissionDenied

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    form = ProjectForm(
        request.POST or None,
        instance=project
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Project berhasil diperbarui!"
        )
        return redirect("main:show_projects")

    context = {
        "name": "Keizora",
        "form": form,
        "form_title": "Edit Project",
        "submit_text": "Simpan Perubahan",
    }

    return render(
        request,
        "projects_form.html",
        context
    )

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Keizora",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', timezone.localtime().strftime("%Y-%m-%d %H:%M:%S"))
        return response

    context = {
        "name": "Keizora",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    if request.method != "POST":
        raise PermissionDenied

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    if project.starred_by.filter(
        pk=request.user.pk
    ).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")

def is_editor(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Editor").exists()
    )

def can_edit(user):
    return user.is_superuser or is_editor(user)
