# domain/tags/tag.py
class Tag:
    def __init__(self, name):
        self._name = name
        self._tasks = []

    def attach_to_task(self, task):
        self._tasks.append(task)
        task.add_tag(self)

    def detach_from_task(self, task):
        self._tasks.remove(task)
        task._tags.remove(self)