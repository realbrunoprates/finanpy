from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm
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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Permite ao usuário editar seu próprio perfil.
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_object(self, queryset=None):
        """
        Retorna sempre o perfil do usuário logado.
        """
        return self.request.user.profile

    def form_valid(self, form):
        """
        Adiciona mensagem de sucesso após salvar o perfil.
        """
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)
