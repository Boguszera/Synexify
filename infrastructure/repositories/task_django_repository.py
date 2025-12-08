from django.db import transaction
from django.apps import apps
from domain.repositories.task_repository import TaskRepository
from domain.tasks.task_base import TaskBase
from infrastructure.orm.mappers.task_mapper import TaskMapper


class TaskDjangoRepository(TaskRepository):

    def get_by_id(self, task_id: str) -> TaskBase | None:
        TaskModel = apps.get_model('orm', 'TaskModel')
        model = TaskModel.objects.filter(id=task_id).first()
        if not model:
            return None
        return TaskMapper.to_domain(model)

    def save(self, task: TaskBase) -> TaskBase:
        TaskModel = apps.get_model('orm', 'TaskModel')
        from infrastructure.orm.models.user_model import UserModel
        from infrastructure.orm.models.tag_model import TagModel

        with transaction.atomic():
            model = TaskModel.objects.filter(id=task.get_id()).first()
            model = TaskMapper.to_orm(task, model)
            model.save()

            # sync many-to-many
            assignees = UserModel.objects.filter(id__in=task.get_assignees_ids())
            model.assignees.set(assignees)

            tags = TagModel.objects.filter(id__in=task.get_tag_ids())
            model.tags.set(tags)

        return TaskMapper.to_domain(model)

    def delete(self, task_id: str) -> None:
        TaskModel = apps.get_model('orm', 'TaskModel')
        TaskModel.objects.filter(id=task_id).delete()

    def get_all(self) -> list[TaskBase]:
        TaskModel = apps.get_model('orm', 'TaskModel')
        return [TaskMapper.to_domain(m) for m in TaskModel.objects.all()]

    def list_by_project(self, project_id: str) -> list[TaskBase]:
        TaskModel = apps.get_model('orm', 'TaskModel')
        models = TaskModel.objects.filter(project_id=project_id)
        return [TaskMapper.to_domain(m) for m in models]

    def list_by_sprint(self, sprint_id: int) -> list[TaskBase]:
        TaskModel = apps.get_model('orm', 'TaskModel')
        models = TaskModel.objects.filter(sprint_id=sprint_id)
        return [TaskMapper.to_domain(m) for m in models]
