# application/attachment_service.py

from domain.users.user_base import UserBase
from domain.attachments.attachment import Attachment
from domain.exceptions.exceptions import PermissionDenied
from django.core.files.uploadedfile import InMemoryUploadedFile

MAX_ATTACHMENTS = 10


class AttachmentService:
    def __init__(self, auth_service, attachment_repo, task_repo):
        self.auth = auth_service
        self.attachment_repo = attachment_repo
        self.task_repo = task_repo

    def add_attachment(self, task_id: str, user: UserBase, file: InMemoryUploadedFile) -> Attachment:
        if self.attachment_repo.count_by_task(task_id) >= MAX_ATTACHMENTS:
            raise PermissionDenied(user.get_id(), action="add_attachment", resource="Max attachments limit")

        if self.attachment_repo.exists_by_filename(file.name, task_id):
            raise ValueError(f"File {file.name} already exists for this task.")

        attachment = Attachment(filename=file.name, uploaded_by=user)
        saved_attachment = self.attachment_repo.save(attachment, task_id, file_data=file)
        task = self.task_repo.get_by_id(task_id)
        if task:
            task.attach_file_id(saved_attachment.get_id())
            self.task_repo.save(task)

        return saved_attachment

    def list_attachments_for_task(self, task_id: str, user: UserBase):
        return self.attachment_repo.list_by_task(task_id)

    def delete_attachment(self, attachment_id: str, user: UserBase) -> None:
        attachment = self.attachment_repo.get_by_id(attachment_id)
        if not attachment:
            return

        if attachment.get_uploaded_by_id() != user.get_id() and user.get_role() not in ["admin", "manager"]:
            raise PermissionDenied(user.get_id(), action="delete_attachment", resource=attachment_id)

        self.attachment_repo.delete(attachment_id)

    def download_attachment(self, attachment_id: str, user: UserBase) -> bytes:
        return self.attachment_repo.get_file_content(attachment_id)