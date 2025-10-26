# Django
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Local imports
from .forms import SignupForm


class SignupView(SuccessMessageMixin, CreateView):
    """
    View para registro de novos usuários com login automático após sucesso.
    """
    form_class = SignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Conta criada com sucesso! Bem-vindo ao Finanpy.'

    def form_valid(self, form):
        """
        Sobrescreve form_valid para fazer login automático após o registro.
        """
        response = super().form_valid(form)

        # Perform automatic login after successful registration
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        return response
