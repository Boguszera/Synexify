# domain/tasks/feature_task.py
from typing import Optional

from .task_base import TaskBase

class FeatureTask(TaskBase):
    def __init__(self, title: str, description: str, story_points: int, task_id: Optional[str] = None, project_id: Optional[str] = None, sprint_id: Optional[str] = None):
        super().__init__(
            title=title,
            description=description,
            task_id=task_id,
            project_id=project_id,
            sprint_id=sprint_id
        )
        self.story_points = story_points
        self.dependencies = []

    def get_story_points(self):
        return self.story_points

    def get_dependencies(self):
        return list(self.dependencies)

    def add_dependency(self, task):
        if task not in self.dependencies:
            self.dependencies.append(task)
