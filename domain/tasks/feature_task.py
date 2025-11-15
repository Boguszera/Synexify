# domain/tasks/feature_task.py
from .task_base import TaskBase

class FeatureTask(TaskBase):
    def __init__(self, task_id, title, description, story_points):
        super().__init__(task_id, title, description)
        self.story_points = story_points
        self.dependencies = []

    def add_dependency(self, task):
        self.dependencies.append(task)