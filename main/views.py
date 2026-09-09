from django.shortcuts import render

from main.models import Experience


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
    context = {
        "name": "Keizora",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)