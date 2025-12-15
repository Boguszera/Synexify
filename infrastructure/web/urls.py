# web/urls.py

from django.urls import path
from .views import project_views, auth_views

app_name = 'web'

urlpatterns = [
    # Auth
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # Projects
    # Główna strona po zalogowaniu
    path('', project_views.project_list, name='project_list'),
    path('projects/create/', project_views.project_create, name='project_create'),
    path('projects/<uuid:pk>/', project_views.project_detail, name='project_detail'), # [FIX] Używamy uuid
]