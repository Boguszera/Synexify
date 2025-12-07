from django.db import transaction
from domain.repositories.task_repository import TaskRepository
from domain.tasks.task_base import TaskBase

from infrastructure.orm.models.task_model import TaskModel
from infrastructure.orm.mappers.task_mapper import TaskMapper
from infrastructure.orm.mappers.comment_mapper import CommentMapper
from infrastructure.orm.mappers.attachment_mapper import AttachmentMapper


class TaskDjangoRepository(TaskRepository):

    def get_by_id(self, task_id: str) -> TaskBase | None:
        model = TaskModel.objects.filter(id=task_id).first()
        if not model:
            return None
        return TaskMapper.to_domain(model)

    def save(self, task: TaskBase) -> TaskBase:
        with transaction.atomic():
            model = TaskModel.objects.filter(id=task.get_id()).first()
            model = TaskMapper.to_orm(task, model)
            model.save()

            # M2M
            TaskMapper.sync_many_to_many(task, model)

            # Comments
            for cid in task.get_comments_ids():
                # sync comments
                pass

            # Attachments
            for aid in task.get_attachment_ids():
                pass

        return TaskMapper.to_domain(model)

    def delete(self, task_id: str) -> None:
        TaskModel.objects.filter(id=task_id).delete()

    def get_all(self) -> list[TaskBase]:
        return [TaskMapper.to_domain(m) for m in TaskModel.objects.all()]

    def list_by_project(self, project_id: str) -> list[TaskBase]:
        models = TaskModel.objects.filter(project_id=project_id)
        return [TaskMapper.to_domain(m) for m in models]

    def list_by_sprint(self, sprint_id: int) -> list[TaskBase]:
        models = TaskModel.objects.filter(sprint_id=sprint_id)
        return [TaskMapper.to_domain(m) for m in models]
