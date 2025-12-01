# application/sprint_service.py
from domain.exceptions.exceptions import PermissionDenied

class SprintService:
    def __init__(self, auth_service, sprint_repo, task_repo):
        self.auth = auth_service
        self.sprint_repo = sprint_repo
        self.task_repo = task_repo

    def create_sprint(self, project, name, start_date, end_date, user):
        if not self.auth.can_manage_project(user, project):
            raise PermissionDenied("Cannot create sprint")
        sprint = project.add_sprint(name, start_date, end_date)
        self.sprint_repo.save(sprint)
        return sprint

    def add_task_to_sprint(self, sprint, task, user):
        if not self.auth.can_manage_project(user, sprint.project):
            raise PermissionDenied("Cannot add task")
        sprint.add_task(task)
        self.sprint_repo.save(sprint)

    def remove_task_from_sprint(self, sprint, task, user):
        if not self.auth.can_manage_project(user, sprint.project):
            raise PermissionDenied("Cannot remove task")
        sprint.remove_task(task)
        self.sprint_repo.save(sprint)

    def get_sprint_tasks(self, sprint, filters=None):
        tasks = sprint.get_tasks()
        return tasks

    def get_completion_rate(self, sprint):
        return sprint.get_completion_rate()
