# application/sprint_service.py

from domain.sprints. sprint_base import SprintBase

class SprintService:
    def __init__(self, auth_service, sprint_repo, project_repo, task_repo):
        self.auth = auth_service
        self.sprint_repo = sprint_repo
        self.project_repo = project_repo
        self.task_repo = task_repo

    # ---- CRUD Sprints ----
    def list_sprints(self, user):
        all_sprints = self.sprint_repo.list_all()
        visible_sprints = []
        for s in all_sprints:
            project = self.project_repo.get_by_id(s.get_project_id())
            if self.can_view(user, s, project):
                visible_sprints.append(s)
        return visible_sprints

    def create_sprint(self, project, name, start_date, end_date, user):
        self.auth.check_manage_project(user, project)

        sprint = SprintBase(
            name=name,
            start_date=start_date,
            end_date=end_date,
            project_id=project.get_id()
        )
        saved_sprint = self.sprint_repo.save(sprint)
        project.add_sprint_id(saved_sprint.get_id())
        self.project_repo.save(project)
        return saved_sprint

    def get_sprint(self, sprint_id:  str):
        return self.sprint_repo.get_by_id(sprint_id)

    def update_sprint(self, sprint:  SprintBase, fields: dict, user):
        project = self.project_repo.get_by_id(sprint.get_project_id())
        self.auth.check_manage_project(user, project)
        allowed_fields = {"name", "start_date", "end_date"}
        for k, v in fields.items():
            if k in allowed_fields:
                setattr(sprint, f"_{k}", v)
        return self.sprint_repo.save(sprint)

    def delete_sprint(self, sprint: SprintBase, user):
        project = self.project_repo.get_by_id(sprint.get_project_id())
        self.auth.check_manage_project(user, project)
        self.sprint_repo.delete(sprint. get_id())

    def add_task_to_sprint(self, sprint, task, user):
        project = self.project_repo.get_by_id(sprint.get_project_id())
        self.auth.check_manage_project(user, project)
        sprint.add_task_id(task.get_id())
        task.set_sprint_id(sprint.get_id())
        self.sprint_repo.save(sprint)
        self.task_repo.save(task)

    def remove_task_from_sprint(self, sprint, task, user):
        project = self.project_repo.get_by_id(sprint.get_project_id())
        self.auth.check_manage_project(user, project)
        sprint.remove_task_id(task.get_id())
        task.set_sprint_id(None)
        self.sprint_repo.save(sprint)
        self.task_repo.save(task)

    def can_view(self, user, sprint, project):
        role = user.get_role()
        if role == "admin":
            return True
        if role in ("manager", "team_member") and user.get_id() in project.get_member_ids():
            return True
        return False