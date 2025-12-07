from django.db import transaction
from django.apps import apps
from domain.repositories.sprint_repository import SprintRepository
from domain.sprints.sprint_base import SprintBase
from infrastructure.orm.mappers.sprint_mapper import SprintMapper


class SprintDjangoRepository(SprintRepository):

    def get_by_id(self, sprint_id: int) -> SprintBase | None:
        SprintModel = apps.get_model('infrastructure', 'SprintModel')
        model = SprintModel.objects.filter(id=sprint_id).first()
        if not model:
            return None
        return SprintMapper.to_domain(model)

    def save(self, sprint: SprintBase) -> SprintBase:
        SprintModel = apps.get_model('infrastructure', 'SprintModel')
        with transaction.atomic():
            model = SprintModel.objects.filter(id=sprint.get_id()).first()
            model = SprintMapper.to_orm(sprint, model)
            model.save()
        return SprintMapper.to_domain(model)

    def get_all(self) -> list[SprintBase]:
        SprintModel = apps.get_model('infrastructure', 'SprintModel')
        return [SprintMapper.to_domain(s) for s in SprintModel.objects.all()]

    def delete(self, sprint_id: int) -> None:
        SprintModel = apps.get_model('infrastructure', 'SprintModel')
        SprintModel.objects.filter(id=sprint_id).delete()

    def list_by_project(self, project_id: int) -> list[SprintBase]:
        SprintModel = apps.get_model('infrastructure', 'SprintModel')
        models = SprintModel.objects.filter(project_id=project_id)
        return [SprintMapper.to_domain(m) for m in models]
