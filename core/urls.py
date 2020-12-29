from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = "core"
urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("main/", views.MainView.as_view(), name="main"),
    path("classroom/<int:pk>", views.ClassroomView.as_view(), name="classroom"),
    path("assignment/<int:pk>", views.AssignmentView.as_view(), name="assignment"),
    path("submission/<int:pk>", views.SubmissionView.as_view(), name="submission"),
    path(
        "assignment_admin/<int:pk>",
        views.AssignmentAdminView.as_view(),
        name="assignment_admin",
    ),
    path(
        "classroom/create",
        views.CreateClassroomView.as_view(),
        name="create_classroom",
    ),
    path(
        "assignment/create/<int:classroom_pk>",
        views.CreateAssignmentView.as_view(),
        name="create_assignment",
    ),
]
