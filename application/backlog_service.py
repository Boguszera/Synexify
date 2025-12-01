class BacklogService:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def get_backlog(self, project, user):
        self.auth_service.check_manage_project(user, project)
        # tasks in projects that are not in any sprint
        backlog_tasks = [
            task for task in project.get_all_tasks()
            if not any(task in sprint.get_tasks() for sprint in project.get_sprints())
        ]
        return backlog_tasks

    def prioritize_task(self, task, priority, user):
        self.auth_service.check_manage_project(user, task.get_project())
        task.set_priority(priority)

    def kanban_board(self, project, user):
        self.auth_service.check_view_project(user, project)
        board = {}
        for status in ["To Do", "In Progress", "Done", "Blocked"]:
            board[status] = [task for task in project.get_all_tasks() if task.get_status() == status]
        return board

    def calendar_view(self, projects, user):
        if projects is None:
            raise ValueError("List of projects must be provided")
        tasks_with_dates = []
        for project in projects:
            if not self.auth_service.can_view_project(user, project):
                continue
            for sprint in project.get_sprints():
                for task in sprint.get_tasks():
                    tasks_with_dates.append({
                        "task": task,
                        "start_date": sprint.get_start_date(),
                        "end_date": sprint.get_end_date()
                    })
        return tasks_with_dates
