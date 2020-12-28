from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = "core"
urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
]
