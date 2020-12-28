from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class ProfileView(LoginRequiredMixin, generic.base.TemplateView):
    template_name = "profile.html"
