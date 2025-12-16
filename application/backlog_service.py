class BacklogService:
    KANBAN_STATUSES = ["To Do", "In Progress", "Done", "Blocked"]

    def __init__(self, auth_service, task_repo, sprint_repo):
        self.auth_service = auth_service
        self.task_repo = task_repo
        self.sprint_repo = sprint_repo

    def kanban_board(self, project, user, sprint_id=None):
        self.auth_service.check_view_project(user, project)
        board = {status: [] for status in self.KANBAN_STATUSES}

        if sprint_id:
            tasks_for_board = self.task_repo.list_by_sprint(sprint_id)
        else:
            tasks_for_board = [t for t in self.task_repo.list_by_project(project.get_id()) if t.get_sprint_id() is None]

        for task in tasks_for_board:
            view_status = task.get_status()
            if view_status in board:
                board[view_status].append(task)

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

    def get_backlog(self, project, user):
        self.auth_service.check_manage_project(user, project)
        all_backlog = self.kanban_board(project, user, sprint_id=None)

        backlog_tasks = []
        for status_list in all_backlog.values():
            backlog_tasks.extend(status_list)

        return backlog_tasks