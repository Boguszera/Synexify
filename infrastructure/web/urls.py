# infrastructure/web/urls.py
from django.urls import path
from .views import project_views, auth_views, task_views, sprint_views, general_views, report_views, tag_views

app_name = 'web'

urlpatterns = [
    # AUTH
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # PROJECTS (Dashboard)
    path('', project_views.project_list, name='project_list'),
    path('projects/create/', project_views.project_create, name='project_create'),
    path('projects/<uuid:pk>/', project_views.project_detail, name='project_detail'),

    # SPRINTS (Kanban Board)
    path('projects/<uuid:project_id>/sprints/create/', sprint_views.sprint_create, name='sprint_create'),
    path('sprints/<uuid:pk>/board/', sprint_views.sprint_board, name='sprint_board'),

    # TASKS (CRUD + Details + Moves)
    path('projects/<uuid:project_id>/tasks/create/', task_views.task_create, name='task_create'),
    path('tasks/<uuid:pk>/', task_views.task_detail, name='task_detail'),
    path('tasks/<uuid:pk>/move/<str:new_status>/', task_views.task_move, name='task_move'),

    # Tasks Operations
    path('tasks/<uuid:pk>/comment/', task_views.add_comment, name='task_add_comment'),
    path('tasks/<uuid:pk>/attach/', task_views.add_attachment, name='task_add_attachment'),
    path('tasks/<uuid:pk>/assign/', task_views.assign_task, name='assign_task'),
    path('tasks/<uuid:pk>/to_sprint/', task_views.add_task_to_sprint, name='add_task_to_sprint'),
    path('tasks/<uuid:pk>/comment/', task_views.add_comment, name='task_add_comment'),
    path('tasks/<uuid:pk>/attach/', task_views.add_attachment, name='task_add_attachment'),
    path('tasks/<uuid:pk>/assign/', task_views.assign_task, name='assign_task'),
    path('tasks/<uuid:pk>/unassign/<uuid:assignee_id>/', task_views.unassign_task, name='unassign_task'),
    path('tasks/my-assignments/', task_views.my_assignments, name='my_assignments'),
path('tasks/<pk>/remove-from-sprint/', task_views.remove_task_from_sprint, name='remove_task_from_sprint'),

    # Notifications
    path('notifications/<uuid:pk>/read/', general_views.mark_notification_read, name='mark_notification_read'),
    path('notifications/clear/', general_views.clear_notifications, name='clear_notifications'),

    # Reports
    path('reports/status/', report_views.report_status_summary, name='report_status'),
    path('reports/workload/', report_views.report_team_workload, name='report_workload'),
    path('reports/velocity/', report_views.report_team_velocity, name='report_velocity'),

    # Tags
    path('manage/tags/', tag_views.tag_list, name='tag_list'),
    path('manage/tags/create/', tag_views.tag_create, name='tag_create'),
    # path('manage/tags/edit/<uuid:pk>/', tag_views.tag_edit, name='tag_edit'),
    path('manage/tags/delete/<uuid:pk>/', tag_views.tag_delete, name='tag_delete'),
]