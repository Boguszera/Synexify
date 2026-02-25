from domain.sprints.sprint_base import SprintBase
from infrastructure.orm.models.sprint_model import SprintModel


class SprintMapper:
    @staticmethod
    def to_domain(model: SprintModel) -> SprintBase:
        sprint = SprintBase(
            sprint_id=str(model.id),
            name=model.name,
            start_date=model.start_date,
            end_date=model.end_date,
            project_id=str(model.project.id) if model.project else None,
        )

        # Populate task ids
        for task in model.tasks.all():
            sprint.add_task_id(str(task.id))
        return sprint

    @staticmethod
    def to_orm(sprint: SprintBase, model: SprintModel | None = None) -> SprintModel:
        if model is None:
            model = SprintModel()
            model.id = sprint.get_id()

        model.name = sprint.get_name()
        model.project_id = sprint.get_project_id()
        model.start_date = sprint.get_start_date()
        model.end_date = sprint.get_end_date()

        return model
