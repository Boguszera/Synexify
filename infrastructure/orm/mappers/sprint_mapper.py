from infrastructure.orm.models.sprint_model import SprintModel
from domain.sprints.sprint_base import SprintBase
from typing import Optional

class SprintMapper:
    @staticmethod
    def to_domain(model: SprintModel) -> SprintBase:
        sprint = SprintBase(
            sprint_id=str(model.id),
            name=model.name,
            start_date=model.start_date,
            end_date=model.end_date,
            project_id=str(model.project.id) if model.project else None
        )

        # Populate task ids
        sprint._task_ids = [str(t.id) for t in model.tasks.all()]
        return sprint

    @staticmethod
    def to_orm(sprint: SprintBase, model: Optional[SprintModel] = None) -> SprintModel:
        if model is None:
            model = SprintModel()
            model.id = sprint.get_id()

        model.name = sprint.get_name()
        model.project_id = sprint.get_project_id()
        model.start_date = getattr(sprint, "_start_date", None)
        model.end_date = getattr(sprint, "_end_date", None)

        return model
