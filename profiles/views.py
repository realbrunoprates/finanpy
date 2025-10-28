from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Exibe os detalhes do perfil do usuário logado.
    """
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """
        Retorna o perfil do usuário logado.
        """
        return self.request.user.profile
