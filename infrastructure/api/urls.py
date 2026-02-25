# infrastructure/api/urls.py (Ostateczna, Czysta Wersja)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth_urls import urlpatterns as auth_patterns
from .views import projects, reporting, sprints, task_attachments, task_comments, tasks, users

router = DefaultRouter()
router.register(r"users", users.UserViewSet, basename="user")
router.register(r"projects", projects.ProjectViewSet, basename="project")
router.register(r"tasks", tasks.TaskViewSet, basename="task")
router.register(r"sprints", sprints.SprintViewSet, basename="sprint")

# --- ZAGNIEŻDŻONE ENDPOINTY (Bazujące na Tasku jako Root) ---

# Rejestracja ViewSetu dla Komentarzy
router.register(r"tasks/(?P<task_pk>[^/.]+)/comments", task_comments.CommentViewSet, basename="task-comments")

# Rejestracja ViewSetu dla Załączników
router.register(
    r"tasks/(?P<task_pk>[^/.]+)/attachments", task_attachments.AttachmentViewSet, basename="task-attachments"
)

urlpatterns = [
    path("", include(router.urls)),
    path("reporting/dashboard/", reporting.DashboardView.as_view()),
    path("auth/", include(auth_patterns)),
]
