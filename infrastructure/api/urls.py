from django.urls import path
from .views import users, projects, tasks, sprints, reporting

urlpatterns = [
    path('users/', users.UserListCreateView.as_view()),
    path('users/<str:pk>/', users.UserDetailView.as_view()),
    path('projects/', projects.ProjectListCreateView.as_view()),
    path('projects/<str:pk>/', projects.ProjectDetailView.as_view()),
    path('tasks/', tasks.TaskListCreateView.as_view()),
    path('tasks/<str:pk>/', tasks.TaskDetailView.as_view()),
    path('sprints/', sprints.SprintListCreateView.as_view()),
    path('sprints/<int:pk>/', sprints.SprintDetailView.as_view()),
    path('reporting/dashboard/', reporting.DashboardView.as_view()),
]
