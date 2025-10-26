# Standard library
from django import forms

# Django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Local imports
User = get_user_model()


class SignupForm(UserCreationForm):
    """
    Formulário de registro de usuário com validação de email único.
    """
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'seu@email.com'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Seu nome de usuário'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure password1 widget with TailwindCSS classes
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Digite sua senha'
        })
        self.fields['password1'].label = 'Senha'

        # Configure password2 widget with TailwindCSS classes
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Confirme sua senha'
        })
        self.fields['password2'].label = 'Confirmar Senha'

        # Update username label
        self.fields['username'].label = 'Nome de Usuário'

    def clean_email(self):
        """
        Valida se o email é único no sistema.
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail.')
        return email

    def clean_username(self):
        """
        Valida se o nome de usuário é único e atende aos requisitos.
        """
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Já existe um usuário com este nome.')
        if len(username) < 3:
            raise forms.ValidationError('O nome de usuário deve ter pelo menos 3 caracteres.')
        return username
