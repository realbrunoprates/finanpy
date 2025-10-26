# Django
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

# Local imports
from .forms import SignupForm, LoginForm


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


class LoginView(FormView):
    """
    View para login de usuários existentes.
    """
    form_class = LoginForm
    template_name = 'auth/login.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        """
        Autentica o usuário com email e senha e faz login se credenciais válidas.
        """
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Authenticate user by email
        # Django authenticate expects username, but we need to find user by email first
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(self.request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # Successful authentication
            login(self.request, user)
            messages.success(self.request, 'Bem-vindo de volta!')
            return super().form_valid(form)
        else:
            # Invalid credentials
            form.add_error(None, 'E-mail ou senha inválidos.')
            return self.form_invalid(form)


class LogoutView(DjangoLogoutView):
    """
    View para logout de usuários autenticados.
    Adiciona mensagem de sucesso ao fazer logout.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Sobrescreve dispatch para adicionar mensagem de sucesso antes do logout.
        """
        if request.user.is_authenticated:
            messages.success(request, 'Você saiu com sucesso.')
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    """
    Página inicial pública com redirecionamento para usuários autenticados.
    """
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """
        Redireciona usuários autenticados para o dashboard.
        """
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return super().get(request, *args, **kwargs)
