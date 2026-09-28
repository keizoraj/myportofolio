from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    show_projects, 
    create_project, 
    get_projects_json, 
    delete_project,
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    show_education,
    create_education,
    update_education,
    delete_education,
    get_education_json,
    register,
    login_user,
    logout_user,
    toggle_star,
    update_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path(
        "experience/<uuid:experience_id>/edit/",
        update_experience,
        name="update_experience",
    ),
    path(
        "experience/<uuid:experience_id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path(
        "api/experience/",
        get_experience_json,
        name="get_experience_json",
    ),

    path("projects/", show_projects, name="show_projects"),

    path(
        "projects/add/",
        create_project,
        name="create_project",
    ),

    path(
        "projects/<uuid:project_id>/edit/",
        update_project,
        name="update_project",
    ),

    path(
        "projects/<uuid:project_id>/delete/",
        delete_project,
        name="delete_project",
    ),

    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),

    path(
        "api/projects/",
        get_projects_json,
        name="get_projects_json",
    ),
    
    path(
    "education/",
    show_education,
    name="show_education",
    ),

    path(
        "education/add/",
        create_education,
        name="create_education",
    ),

    path(
        "education/<uuid:education_id>/edit/",
        update_education,
        name="update_education",
    ),

    path(
        "education/<uuid:education_id>/delete/",
        delete_education,
        name="delete_education",
    ),

    path(
        "api/education/",
        get_education_json,
        name="get_education_json",
    ),

    path(
        "register/", 
        register, 
        name="register"
    ),
    path(
        "login/", 
        login_user, 
        name="login"
    ),
    path(
        "logout/", 
        logout_user, 
        name="logout"
    ),

    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),

    path(
    "projects/<uuid:project_id>/edit/",
    update_project,
    name="update_project",
    ),
]