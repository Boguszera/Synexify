# application/sprint_service.py

class SprintService:
    def __init__(self, auth_service, sprint_repo, project_repo):
        self.auth = auth_service
        self.sprint_repo = sprint_repo
        self.project_repo = project_repo

    def create_sprint(self, project, name, start_date, end_date, user):
        self.auth.check_manage_project(user, project)
        sprint = project.add_sprint(name, start_date, end_date)
        self.sprint_repo.save(sprint)
        self.project_repo.save(project)
        return sprint

    def add_task_to_sprint(self, sprint, task, user):
        self.auth.check_manage_project(user, sprint.get_project())
        sprint.add_task_id(task.get_id())
        self.sprint_repo.save(sprint)

    def remove_task_from_sprint(self, sprint, task, user):
        self.auth.check_manage_project(user, sprint.get_project())
        sprint.remove_task_id(task.get_id())
        self.sprint_repo.save(sprint)

    def get_all(self):
        return self.sprint_repo.list_all()

    """    
    def get_sprint_tasks(self, sprint, filters=None):
        tasks = sprint.get_tasks()
        return tasks

    def get_completion_rate(self, sprint):
        return sprint.get_completion_rate()
    """