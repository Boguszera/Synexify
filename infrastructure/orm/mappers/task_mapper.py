# infrastructure/orm/mappers/task_mapper.py

from infrastructure.orm.models.task_model import TaskModel
from infrastructure.orm.models.user_model import UserModel
from domain.tasks.task_base import TaskBase
from domain.tasks.bug_task import BugTask
from domain.tasks.feature_task import FeatureTask
from domain.tasks.chore_task import ChoreTask
from typing import Optional, Callable, List


class TaskMapper:

    @staticmethod
    def to_domain(model: TaskModel) -> TaskBase:
        task_type = getattr(model, 'task_type', 'chore')

        common_args = {
            'task_id': str(model.id),
            'title': model.title,
            'description': model.description,
            'project_id': str(model.project.id) if model.project else None,
            'sprint_id': model.sprint.id if model.sprint else None,
        }

        if task_type == "bug" and hasattr(model, 'severity'):
            task = BugTask(severity=getattr(model, 'severity', None), **common_args)
        elif task_type == "feature" and hasattr(model, 'story_points'):
            task = FeatureTask(story_points=getattr(model, 'story_points', None), **common_args)
        else:
            task = TaskBase(**common_args)

        task._status = model.status

        if not hasattr(task, '_task_type'):
            task._task_type = task_type

        # Mapowanie relacji M2M jest OK
        task._assignee_ids = [str(u.id) for u in model.assignees.all()]
        task._tag_ids = [str(t.id) for t in model.tags.all()]
        task._comment_ids = [str(c.id) for c in model.comments.all()]
        task._attachment_ids = [str(a.id) for a in model.attachments.all()]

        return task

    @staticmethod
    def to_orm(task: TaskBase, model: Optional[TaskModel] = None) -> TaskModel:
        if model is None:
            model = TaskModel(id=task.get_id())

        model.title = task.get_title()
        model.description = task.get_description()
        model.status = task.get_status()

        # FK
        model.project_id = task.get_project_id() if task.get_project_id() else None
        model.sprint_id = task.get_sprint_id() if task.get_sprint_id() else None

        return model