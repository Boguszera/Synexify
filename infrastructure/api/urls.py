from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import users, projects, tasks, sprints, reporting
from .auth_urls import urlpatterns as auth_patterns

router = DefaultRouter()
router.register(r'users', users.UserViewSet, basename='user')
router.register(r'projects', projects.ProjectViewSet, basename='project')
router.register(r'tasks', tasks.TaskViewSet, basename='task')
router.register(r'sprints', sprints.SprintViewSet, basename='sprint')

urlpatterns = [
    path('', include(router.urls)),
    path('reporting/dashboard/', reporting.DashboardView.as_view()),
    path('auth/', include(auth_patterns)),
]