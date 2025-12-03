from typing import List, Dict, Optional
from domain.interfaces.reportable import Reportable
import uuid

class ProjectBase(Reportable):
    def __init__(self, name: str, description: str, project_id: Optional[str] = None):
        if project_id is not None and not isinstance(project_id, str):
            raise TypeError("project_id must be a string UUID or None")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        self._id = project_id or str(uuid.uuid4())
        self._name = name
        self._description = description
        self._member_ids: List[str] = []
        self._task_ids: List[str] = []
        self._sprint_ids: List[int] = []
        self._archived: bool = False

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_member_ids(self) -> List[str]:
        return list(self._member_ids)

    def get_task_ids(self) -> List[str]:
        return list(self._task_ids)

    def get_sprint_ids(self) -> List[int]:
        return list(self._sprint_ids)

    def add_member_id(self, user_id: str):
        if user_id in self._member_ids:
            return
        self._member_ids.append(user_id)

    def remove_member_id(self, user_id: str):
        if user_id not in self._member_ids:
            raise ValueError("User not a member")
        self._member_ids.remove(user_id)

    def add_task_id(self, task_id: str):
        if task_id in self._task_ids:
            return
        self._task_ids.append(task_id)

    def add_sprint_id(self, sprint_id: int):
        if sprint_id in self._sprint_ids:
            return
        self._sprint_ids.append(sprint_id)

    def get_report_data(self, task_loader_callable=None) -> Dict:
        total_tasks = len(self._task_ids)
        if task_loader_callable:
            tasks = [task_loader_callable(tid) for tid in self._task_ids]
            done_tasks = len([t for t in tasks if t.get_status().lower() == "done"])
            completion = (done_tasks / total_tasks * 100) if total_tasks else 0.0
        else:
            done_tasks = 0
            completion = 0.0

        return {
            "project_name": self.get_name(),
            "total_tasks": total_tasks,
            "tasks_done": done_tasks,
            "completion_percentage": completion,
            "members_count": len(self._member_ids),
            "members": list(self._member_ids)
        }