# infrastructure/orm/mappers/task_mapper.py

from infrastructure.orm.models.task_model import TaskModel
from domain.tasks.task_base import TaskBase
from domain.tasks.bug_task import BugTask
from domain.tasks.feature_task import FeatureTask
from domain.tasks.chore_task import ChoreTask
from typing import Optional, List
from django.apps import apps

STATUS_MAPPING = {
    "todo": "To Do",
    "in_progress": "In Progress",
    "done": "Done",
    "blocked": "Blocked"
}
STATUS_DB_TO_DOMAIN = STATUS_MAPPING
STATUS_DOMAIN_TO_DB = {v: k for k, v in STATUS_MAPPING.items()}

class TaskMapper:

    @staticmethod
    def to_domain(model: TaskModel) -> TaskBase:
        task_type = getattr(model, 'task_type', 'chore')

        assignee_ids = [str(u.id) for u in model.assignees.all()]
        tag_ids = [str(t.id) for t in model.tags.all()]

        comment_ids = [str(c.id) for c in model.comments.all()]
        attachment_ids = [str(a.id) for a in model.attachments.all()]

        common_args = {
            'task_id': str(model.id),
            'title': model.title,
            'description': model.description,
            'project_id': str(model.project_id) if model.project_id else None,
            'sprint_id': str(model.sprint_id) if model.sprint_id else None,
        }

        if task_type == "bug":
            task = BugTask(
                severity=getattr(model, 'severity', None),
                **common_args
            )
        elif task_type == "feature":
            task = FeatureTask(
                story_points=getattr(model, 'story_points', None),
                **common_args
            )
        else:
            task = ChoreTask(**common_args)
        domain_status = STATUS_DB_TO_DOMAIN.get(model.status, model.status)
        task._status = domain_status

        task._assignee_ids = assignee_ids
        task._tag_ids = tag_ids
        task._comment_ids = comment_ids
        task._attachment_ids = attachment_ids

        return task

    @staticmethod
    def to_orm(task: TaskBase, model: Optional[TaskModel] = None) -> TaskModel:
        if model is None:
            model = TaskModel(id=task.get_id())

        model.title = task.get_title()
        model.description = task.get_description()

        model.status = STATUS_DOMAIN_TO_DB.get(task.get_status(), task.get_status())

        # FK
        model.project_id = task.get_project_id()
        model.sprint_id = task.get_sprint_id()

        if isinstance(task, BugTask):
            model.task_type = 'bug'
            model.severity = task.get_severity()
            model.story_points = None
        elif isinstance(task, FeatureTask):
            model.task_type = 'feature'
            model.story_points = task.get_story_points()
            model.severity = None
        else:
            model.task_type = 'chore'
            model.severity = None
            model.story_points = None

        return model