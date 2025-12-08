from django.db import transaction
from django.apps import apps
from domain.repositories.sprint_repository import SprintRepository
from domain.sprints.sprint_base import SprintBase
from infrastructure.orm.mappers.sprint_mapper import SprintMapper


class SprintDjangoRepository(SprintRepository):

    def get_by_id(self, sprint_id: str) -> SprintBase | None:
        SprintModel = apps.get_model('orm', 'SprintModel')
        model = SprintModel.objects.filter(id=sprint_id).first()
        if not model:
            return None
        return SprintMapper.to_domain(model)

    def save(self, sprint: SprintBase) -> SprintBase:
        SprintModel = apps.get_model('orm', 'SprintModel')
        with transaction.atomic():
            model = SprintModel.objects.filter(id=sprint.get_id()).first()
            model = SprintMapper.to_orm(sprint, model)
            model.save()
        return SprintMapper.to_domain(model)

    def delete(self, sprint_id: str) -> None:
        SprintModel = apps.get_model('orm', 'SprintModel')
        SprintModel.objects.filter(id=sprint_id).delete()

    def list_by_project(self, project_id: str) -> list[SprintBase]:
        SprintModel = apps.get_model('orm', 'SprintModel')
        models = SprintModel.objects.filter(project_id=project_id)
        return [SprintMapper.to_domain(m) for m in models]

