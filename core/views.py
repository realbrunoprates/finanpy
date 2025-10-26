# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard temporário enquanto funcionalidades principais são desenvolvidas.
    """
    template_name = 'dashboard.html'
    login_url = '/auth/login/'
