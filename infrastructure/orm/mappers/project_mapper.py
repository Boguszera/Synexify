# infrastructure/orm/mappers/project_mapper.py
from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.user_model import UserModel
from domain.projects.project_base import ProjectBase
from typing import Optional


class ProjectMapper:
    @staticmethod
    def to_domain(model: ProjectModel) -> ProjectBase:
        project = ProjectBase(
            name=model.name,
            description=model.description,
            project_id=str(model.id)
        )

        for member in model.members.all():
            project.add_member_id(str(member.id))

        for task in model.tasks.all():
            project.add_task_id(str(task.id))

        for sprint in model.sprints.all():
            project.add_sprint_id(str(sprint.id))

        return project

    @staticmethod
    def to_orm(project: ProjectBase, model: Optional[ProjectModel] = None) -> ProjectModel:
        if model is None:
            model = ProjectModel(id=project.get_id())

        model.name = project.get_name()
        model.description = project.get_description()
        model.archived = project.get_archived()

        return model