from django.db import transaction
from domain.repositories.sprint_repository import SprintRepository
from domain.sprints.sprint_base import SprintBase

from infrastructure.orm.models.sprint_model import SprintModel
from infrastructure.orm.mappers.sprint_mapper import SprintMapper


class SprintDjangoRepository(SprintRepository):

    def get_by_id(self, sprint_id: int) -> SprintBase | None:
        model = SprintModel.objects.filter(id=sprint_id).first()
        if not model:
            return None
        return SprintMapper.to_domain(model)

    def save(self, sprint: SprintBase) -> SprintBase:
        with transaction.atomic():
            model = SprintModel.objects.filter(id=sprint.get_id()).first()
            model = SprintMapper.to_orm(sprint, model)
            model.save()

        return SprintMapper.to_domain(model)

    def get_all(self) -> list[SprintBase]:
        return [SprintMapper.to_domain(s) for s in SprintModel.objects.all()]

    def delete(self, sprint_id: int) -> None:
        SprintModel.objects.filter(id=sprint_id).delete()

    def list_by_project(self, project_id: int) -> list[SprintBase]:
        models = SprintModel.objects.filter(project_id=project_id)
        return [SprintMapper.to_domain(m) for m in models]
