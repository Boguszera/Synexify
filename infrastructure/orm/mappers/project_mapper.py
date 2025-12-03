# infrastructure/orm/mappers/project_mapper.py
from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.user_model import UserModel
from domain.projects.project_base import ProjectBase
from typing import Optional, Callable

class ProjectMapper:
    @staticmethod
    def to_domain(model: ProjectModel) -> ProjectBase:
        project = ProjectBase(
            name=model.name,
            description=model.description,
            project_id=str(model.id)
        )

        # Members
        project._member_ids = [str(u.id) for u in model.members.all()]
        # Tasks
        project._task_ids = [str(t.id) for t in model.tasks.all()]
        # Sprints
        project._sprint_ids = [s.id for s in model.sprints.all()]

        project._archived = model.archived
        return project

    @staticmethod
    def to_orm(project: ProjectBase, model: Optional[ProjectModel] = None) -> ProjectModel:
        if model is None:
            model = ProjectModel(id=project.get_id())

        model.name = project.get_name()
        model.description = project.get_description()
        model.archived = getattr(project, "_archived", False)

        return model

    @staticmethod
    def sync_many_to_many(project: ProjectBase, model: ProjectModel):
        members = UserModel.objects.filter(id__in=project.get_member_ids())
        model.members.set(members)
