class BacklogService:
    def __init__(self, auth_service, task_repo):
        self.auth_service = auth_service
        self.task_repo = task_repo

    def get_backlog(self, project, user):
        self.auth_service.check_manage_project(user, project)
        backlog_tasks = []
        for task_id in project.get_task_ids():
            task = self.task_repo.get(task_id)
            if not task:
                continue
            if not any(task.get_id() in sprint.get_task_ids() for sprint in project.get_sprints()):
                backlog_tasks.append(task)
        return backlog_tasks

    def prioritize_task(self, task, priority, user):
        self.auth_service.check_manage_project(user, task.get_project())
        task.set_priority(priority)

    def kanban_board(self, project, user):
        self.auth_service.check_view_project(user, project)
        board = {status: [] for status in ["To Do", "In Progress", "Done", "Blocked"]}
        for task_id in project.get_task_ids():
            task = self.task_repo.get(task_id)
            if task:
                board.get(task.get_status(), []).append(task)
        return board

    def calendar_view(self, projects, user):
        if projects is None:
            raise ValueError("List of projects must be provided")
        tasks_with_dates = []
        for project in projects:
            if not self.auth_service.can_view_project(user, project):
                continue
            for sprint in project.get_sprints():
                for task_id in sprint.get_task_ids():
                    task = self.task_repo.get(task_id)
                    if task:
                        tasks_with_dates.append({
                            "task": task,
                            "start_date": sprint.get_start_date(),
                            "end_date": sprint.get_end_date()
                        })
        return tasks_with_dates
