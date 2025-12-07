from django.db import transaction
from django.apps import apps
from domain.repositories.project_repository import ProjectRepository
from domain.projects.project_base import ProjectBase
from infrastructure.orm.mappers.project_mapper import ProjectMapper


class ProjectDjangoRepository(ProjectRepository):

    def get_by_id(self, project_id: str) -> ProjectBase | None:
        ProjectModel = apps.get_model('infrastructure', 'ProjectModel')
        model = ProjectModel.objects.filter(id=project_id).first()
        if not model:
            return None
        return ProjectMapper.to_domain(model)

    def save(self, project: ProjectBase) -> ProjectBase:
        ProjectModel = apps.get_model('infrastructure', 'ProjectModel')
        from infrastructure.orm.models.user_model import UserModel

        with transaction.atomic():
            model = ProjectModel.objects.filter(id=project.get_id()).first()
            model = ProjectMapper.to_orm(project, model)
            model.save()

            # sync M2M
            members = UserModel.objects.filter(id__in=project.get_member_ids())
            model.members.set(members)

        return ProjectMapper.to_domain(model)

    def list_all(self) -> list[ProjectBase]:
        ProjectModel = apps.get_model('infrastructure', 'ProjectModel')
        return [ProjectMapper.to_domain(p) for p in ProjectModel.objects.all()]

    def delete(self, project_id: str) -> None:
        ProjectModel = apps.get_model('infrastructure', 'ProjectModel')
        ProjectModel.objects.filter(id=project_id).delete()
