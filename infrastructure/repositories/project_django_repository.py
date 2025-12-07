from django.db import transaction
from domain.repositories.project_repository import ProjectRepository
from domain.projects.project_base import ProjectBase

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.mappers.project_mapper import ProjectMapper


class ProjectDjangoRepository(ProjectRepository):

    def get_by_id(self, project_id: str) -> ProjectBase | None:
        model = ProjectModel.objects.filter(id=project_id).first()
        if not model:
            return None
        return ProjectMapper.to_domain(model)

    def save(self, project: ProjectBase) -> ProjectBase:
        with transaction.atomic():
            model = ProjectModel.objects.filter(id=project.get_id()).first()
            model = ProjectMapper.to_orm(project, model)
            model.save()

            # sync M2M
            ProjectMapper.sync_many_to_many(project, model)

        return ProjectMapper.to_domain(model)

    def list_all(self) -> list[ProjectBase]:
        return [ProjectMapper.to_domain(p) for p in ProjectModel.objects.all()]

    def delete(self, project_id: str) -> None:
        ProjectModel.objects.filter(id=project_id).delete()
