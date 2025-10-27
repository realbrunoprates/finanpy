# Django imports
from django.urls import path

# Local imports
from . import views

app_name = 'categories'

urlpatterns = [
    # List all user's categories
    path('', views.CategoryListView.as_view(), name='category_list'),

    # Create new category
    path('new/', views.CategoryCreateView.as_view(), name='category_create'),

    # Update existing category
    path('<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),

    # Delete existing category
    path('<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
