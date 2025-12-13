# infrastructure/repositories/attachment_django_repository.py

from django.db import transaction
from django.apps import apps
from django.conf import settings
from domain.repositories.attachment_repository import AttachmentRepository
from domain.attachments.attachment import Attachment
from infrastructure.orm.mappers.attachment_mapper import AttachmentMapper
from typing import Optional, List
import os

ATTACHMENT_ROOT = os.path.join(settings.BASE_DIR, 'media', 'attachments')

class AttachmentDjangoRepository(AttachmentRepository):
    def __init__(self, user_repo):
        if not hasattr(settings, 'MEDIA_ROOT'):
            raise RuntimeError("MEDIA_ROOT is not defined in settings")
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, 'attachments')
        os.makedirs(self.upload_dir, exist_ok=True)
        self.user_repo = user_repo

    def get_by_id(self, attachment_id: str) -> Optional[Attachment]:
        AttachmentModel = apps.get_model('orm', 'AttachmentModel')
        try:
            model = AttachmentModel.objects.get(id=attachment_id)
            return AttachmentMapper.to_domain(model)
        except AttachmentModel.DoesNotExist:
            return None

    def save(self, attachment: Attachment, task_id: str, file_data=None) -> Attachment:
        AttachmentModel = apps.get_model('orm', 'AttachmentModel')
        with transaction.atomic():
            model_data = AttachmentMapper.to_orm(attachment, task_id)
            orm_obj, _ = AttachmentModel.objects.update_or_create(
                id=model_data.id,
                defaults={
                    'filename': model_data.filename,
                    'task_id': model_data.task_id,
                    'uploaded_by_id': model_data.uploaded_by_id,
                }
            )
            if file_data:
                file_path = os.path.join(ATTACHMENT_ROOT, f"{orm_obj.id}_{orm_obj.filename}")
                with open(file_path, 'wb+') as destination:
                    for chunk in file_data.chunks():
                        destination.write(chunk)
        return self.get_by_id(attachment.get_id())

    def delete(self, attachment_id: str) -> None:
        AttachmentModel = apps.get_model('orm', 'AttachmentModel')
        try:
            obj = AttachmentModel.objects.get(id=attachment_id)
            file_path = os.path.join(ATTACHMENT_ROOT, f"{obj.id}_{obj.filename}")
            if os.path.exists(file_path):
                os.remove(file_path)
            obj.delete()
        except AttachmentModel.DoesNotExist:
            pass

    def list_by_task(self, task_id: str) -> List[Attachment]:
        AttachmentModel = apps.get_model('orm', 'AttachmentModel')
        models = AttachmentModel.objects.filter(task_id=task_id).order_by('uploaded_at')
        return [AttachmentMapper.to_domain(m) for m in models]

    def count_by_task(self, task_id: str) -> int:
        AttachmentModel = apps.get_model('orm', 'AttachmentModel')
        return AttachmentModel.objects.filter(task_id=task_id).count()

    def exists_by_filename(self, filename: str, task_id: str) -> bool:
        AttachmentModel = apps.get_model('orm', 'AttachmentModel')
        return AttachmentModel.objects.filter(filename=filename, task_id=task_id).exists()

    def get_file_content(self, attachment_id: str) -> bytes:
        AttachmentModel = apps.get_model('orm', 'AttachmentModel')
        obj = AttachmentModel.objects.get(id=attachment_id)
        file_path = os.path.join(ATTACHMENT_ROOT, f"{obj.id}_{obj.filename}")
        with open(file_path, 'rb') as f:
            return f.read()