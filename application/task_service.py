# application/task_service.py
from domain.exceptions.exceptions import PermissionDenied
from domain.tasks.bug_task import BugTask
from domain.tasks.feature_task import FeatureTask
from domain.tasks.chore_task import ChoreTask
import uuid
from domain.comments.comment import Comment
from domain.attachments.attachment import Attachment

# Mapowanie slugów z interfejsu/URL na KANONICZNY format DOMENOWY (np. "To Do")
CANONICAL_STATUS_MAP = {
    "todo": "To Do",
    "in_progress": "In Progress",
    "done": "Done",
    "blocked": "Blocked",
}


class TaskService:
    def __init__(self, auth_service, task_repo, project_repo, notification_service, user_repo, attachment_repo,
                 comment_repo):
        self.auth = auth_service
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.notifications = notification_service
        self.user_repo = user_repo
        self.attachment_repo = attachment_repo
        self.comment_repo = comment_repo

    def create_task(self, project, title, description, task_type, user, severity=None, story_points=None):
        self.auth.check_manage_project(user, project)
        task_id = str(uuid.uuid4())
        project_id = project.get_id()  # Pobieramy Project ID

        # Dodanie project_id do konstruktorów tasków:

        if task_type == "bug":
            task = BugTask(title=title, description=description, severity=severity, task_id=task_id,
                           project_id=project_id)
        elif task_type == "feature":
            task = FeatureTask(title=title, description=description, story_points=story_points, task_id=task_id,
                               project_id=project_id)
        elif task_type == "chore":
            task = ChoreTask(title=title, description=description, task_id=task_id,
                             project_id=project_id)  # <-- POPRAWKA!
        else:
            raise ValueError("Invalid task type")

        # Ustawienie domyślnego statusu w kanonicznym formacie ("To Do")
        task.update_status(CANONICAL_STATUS_MAP["todo"])

        # WAŻNE: Odświeżamy Project, aby odnotował nowy Task ID
        project.add_task_id(task.get_id())

        # Zapisujemy Task, który teraz ma już przypisany _project_id
        self.task_repo.save(task)
        self.project_repo.save(project)  # Zapisujemy projekt z nowym task_id
        return task

    def assign_task_by_id(self, task, user, assignee_id: str):
        assignee = self.user_repo.get_by_id(assignee_id)
        if assignee is None:
            raise ValueError(f"Assignee user ID {assignee_id} not found.")
        if not self.auth.can_assign_task(user, task):
            if user.get_id() != assignee.get_id():
                raise PermissionDenied(user.get_id(), action="assign_task_other", resource=f"task:{task.get_id()}")
        task.assign_user_id(assignee.get_id())
        self.task_repo.save(task)

        from domain.events.task_events import TaskAssignedEvent
        event = TaskAssignedEvent(task_id=task.get_id(), assigned_user_id=assignee.get_id())
        self.notifications.notify(event)

    def update_status(self, task, user, new_status_raw):
        """
        Aktualizuje status. Oczekuje, że new_status_raw jest slugiem (np. 'in_progress')
        lub kanoniczną nazwą ('In Progress'). Mapuje go na kanoniczną formę dla domeny.
        """
        if not self.auth.can_edit_task(user, task):
            raise PermissionDenied(user.get_id(), action="update_status", resource=f"task:{task.get_id()}")

        # Normalizacja statusu: 'in_progress' -> 'In Progress'.
        # Jeśli już jest kanoniczny ('In Progress'), zostaje niezmieniony.
        # Używamy get(slug, surowa_wartosc) na wypadek, gdyby przyszła nazwa kanoniczna.
        normalized_status = CANONICAL_STATUS_MAP.get(new_status_raw.lower().replace(" ", "_"), new_status_raw)

        old_status = task.get_status()  # Stary status (w formacie kanonicznym)

        # Przekazanie do domeny kanonicznego statusu
        task.update_status(normalized_status)
        self.task_repo.save(task)

        from domain.events.task_events import TaskStatusChangedEvent
        event = TaskStatusChangedEvent(
            task_id=task.get_id(),
            old_status=old_status,
            new_status=normalized_status  # Używamy znormalizowanego statusu
        )
        self.notifications.notify(event)

        return task

    def add_comment(self, task, user, content):
        project = self.project_repo.get_by_id(task.get_project_id())
        self.auth.check_view_project(user, project)

        comment = Comment(content=content, author=user)
        task.add_comment(comment.get_id(), comment.get_author())
        self.task_repo.save(task)

        self.comment_repo.save(comment, task.get_id())

        from domain.events.task_events import TaskCommentAddedEvent
        event = TaskCommentAddedEvent(
            task_id=task.get_id(),
            comment_id=comment.get_id(),
            commenter_id=user.get_id()
        )
        self.notifications.notify(event)
        return comment

    def add_tag(self, task, tag):
        task.add_tag_id(tag.get_id())
        self.task_repo.save(task)

    def remove_tag(self, task, tag):
        task.remove_tag_id(tag.get_id())
        self.task_repo.save(task)

    def get_task_filters(self, project=None, user=None, status=None, tag=None, priority=None):
        tasks = self.task_repo.get_all()

        if project:
            tasks = [t for t in tasks if t.get_project_id() == project.get_id()]
        # if user:
        #    tasks = [t for t in tasks if user.get_id() in t.get_assignees_ids()]
        if status:
            tasks = [t for t in tasks if t.get_status() == status]
        if tag:
            tasks = [t for t in tasks if any(tid == tag.get_id() for tid in t.get_tag_ids())]
        visible_tasks = []
        project_cache = {}
        for task in tasks:
            pid = task.get_project_id()
            if pid not in project_cache:
                project_cache[pid] = self.project_repo.get_by_id(pid)
            proj = project_cache[pid]
            if proj and self.auth.can_view_project(user, proj):
                visible_tasks.append(task)
        return visible_tasks

    def get_task_filters(self, project=None, user=None, status=None, tag=None, priority=None):
        tasks = self.task_repo.get_all()

        if project:
            tasks = [t for t in tasks if t.get_project_id() == project.get_id()]

        if status:
            # UWAGA: status z query_params musi być również w formacie kanonicznym, jeśli jest filtrowany
            tasks = [t for t in tasks if t.get_status() == status]

        if tag:
            tasks = [t for t in tasks if any(tid == tag.get_id() for tid in t.get_tag_ids())]

        visible_tasks = []
        project_cache = {}

        for task in tasks:
            pid = task.get_project_id()
            if pid not in project_cache:
                project_cache[pid] = self.project_repo.get_by_id(pid)

            proj = project_cache[pid]
            if proj and self.auth.can_view_project(user, proj):
                visible_tasks.append(task)

        return visible_tasks

    def update_task(self, task, user, **fields):
        project_id = task.get_project_id()
        project = self.project_repo.get_by_id(project_id)

        if project is None:
            raise PermissionDenied(user.get_id(), action="update_task", resource="Project Not Found")
        self.auth.check_manage_project(user, project)
        allowed_fields = {"title", "description"}

        status_changed = False
        new_status = None

        for key, value in fields.items():
            if key in allowed_fields:
                try:
                    setter_method = getattr(task, f"set_{key}", None)
                    if callable(setter_method):
                        setter_method(value)
                    else:
                        setattr(task, f"_{key}", value)
                except AttributeError:
                    pass

            elif key == "status":
                new_status = value
                status_changed = True

            elif key == "assignee_id":
                self.assign_task_by_id(task, user, value)

        saved_task = self.task_repo.save(task)

        if status_changed and new_status:
            # Używamy nowej metody update_status, która normalizuje status
            return self.update_status(saved_task, user, new_status)
        return saved_task

    def delete_task(self, task_id: str, user):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return
        project = self.project_repo.get_by_id(task.get_project_id())
        self.auth.check_manage_project(user, project)
        self.task_repo.delete(task_id)

    def get_comment_by_id(self, comment_id: str):
        return self.comment_repo.get_by_id(comment_id)

    def get_attachment_by_id(self, attachment_id: str):
        return self.attachment_repo.get_by_id(attachment_id)