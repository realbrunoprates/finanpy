# Django imports
from django.urls import path

# Local imports
from . import views

app_name = 'accounts'

urlpatterns = [
    # List all user's accounts
    path('', views.AccountListView.as_view(), name='list'),

    # Create new account
    path('new/', views.AccountCreateView.as_view(), name='create'),

    # Update existing account
    path('<int:pk>/edit/', views.AccountUpdateView.as_view(), name='update'),

    # Delete existing account
    path('<int:pk>/delete/', views.AccountDeleteView.as_view(), name='delete'),
]
