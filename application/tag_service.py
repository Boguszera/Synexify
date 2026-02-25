import uuid

from domain.exceptions.exceptions import PermissionDenied
from domain.tags.tag import Tag
from domain.tasks.task_base import TaskBase
from domain.users.user_base import UserBase


class TagService:
    def __init__(self, auth_service, task_repo, tag_repo, project_repo):
        self.auth_service = auth_service
        self.task_repo = task_repo
        self.tag_repo = tag_repo
        self.project_repo = project_repo

    def add_tag_to_task(self, task: TaskBase, user: UserBase, tag_id: str):
        project = self.task_repo.get_by_id(task.get_id()).get_project_id()
        if not self.auth_service.can_manage_project(user, self.project_repo.get_by_id(project)):
            raise PermissionDenied(user.get_id(), action="add_tag", resource=f"task:{task.get_id()}")

        tag = self.tag_repo.get_by_id(tag_id)
        if not tag:
            raise ValueError(f"Tag ID {tag_id} not found.")

        task.add_tag_id(tag_id)
        self.task_repo.save(task)
        return task

    def remove_tag_from_task(self, task: TaskBase, user: UserBase, tag_id: str):
        project = self.task_repo.get_by_id(task.get_id()).get_project_id()
        if not self.auth_service.can_manage_project(user, self.project_repo.get_by_id(project)):
            raise PermissionDenied(user.get_id(), action="remove_tag", resource=f"task:{task.get_id()}")

        task.remove_tag_id(tag_id)
        self.task_repo.save(task)
        return task

    def create_tag(self, name: str, user: UserBase) -> Tag:
        if not self.auth_service.is_admin_or_manager(user):
            raise PermissionDenied(user.get_id(), action="create_tag", resource="Tag")

        tag_id = str(uuid.uuid4())
        new_tag = Tag(tag_id=tag_id, name=name)

        return self.tag_repo.save(new_tag)

    def delete_tag(self, tag_id: str, user: UserBase):
        if not self.auth_service.is_admin_or_manager(user):
            raise PermissionDenied(user.get_id(), action="delete_tag", resource="Tag")
        tag_to_delete = self.tag_repo.get_by_id(tag_id)
        if not tag_to_delete:
            raise ValueError("Tag not found.")
        self.tag_repo.delete(tag_id)

    def list_all_tags(self, user: UserBase) -> list[Tag]:
        return self.tag_repo.list_all()
