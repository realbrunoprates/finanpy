# Django
from django.urls import path

# Local imports
from . import views

app_name = 'users'

urlpatterns = [
    path('cadastro/', views.SignupView.as_view(), name='signup'),
]
