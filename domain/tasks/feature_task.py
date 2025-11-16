# domain/tasks/feature_task.py
from .task_base import TaskBase

class FeatureTask(TaskBase):
    def __init__(self, task_id: int, title: str, description: str, story_points: int):
        super().__init__(task_id, title, description)
        self.story_points = story_points
        self.dependencies = []

    def get_story_points(self):
        return self.story_points

    def get_dependencies(self):
        return list(self.dependencies)

    def add_dependency(self, task):
        if task not in self.dependencies:
            return
        self.dependencies.append(task)