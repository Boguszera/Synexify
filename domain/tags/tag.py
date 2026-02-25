# domain/tags/tag.py
class Tag:
    def __init__(self, tag_id: str, name: str):
        if not name or not name.strip():
            raise ValueError("Tag name cannot be empty")
        self._id = tag_id
        self._name = name

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    """
    def get_tasks(self) -> List[TaskBase]:
        return list(self._tasks)

    def attach_to_task(self, task: TaskBase):
        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")
        if task not in self._tasks:
            self._tasks.append(task)
            task.add_tag(self)

    def detach_from_task(self, task: TaskBase):
        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")
        if task in self._tasks:
            self._tasks.remove(task)
            task.remove_tag(self)
    """
