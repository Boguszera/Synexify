from django.urls import path
from .views import project_views, auth_views, task_views, sprint_views  # [NOWY IMPORT]

app_name = 'web'

urlpatterns = [
    # ... Auth ...
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # ... Projects ...
    path('', project_views.project_list, name='project_list'),
    path('projects/create/', project_views.project_create, name='project_create'),
    path('projects/<uuid:pk>/', project_views.project_detail, name='project_detail'),

    # ... Sprints [NOWE] ...
    # Tworzenie nowego sprintu dla danego projektu
    path('projects/<uuid:project_id>/sprints/create/', sprint_views.sprint_create, name='sprint_create'),

    # ... Tasks ...
    path('projects/<uuid:project_id>/tasks/create/', task_views.task_create, name='task_create'),
    path('tasks/<uuid:pk>/move/<str:new_status>/', task_views.task_move, name='task_move'),
]