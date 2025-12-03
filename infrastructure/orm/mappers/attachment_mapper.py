# infrastructure/orm/mappers/attachment_mapper.py
from infrastructure.orm.models.attachment_model import AttachmentModel
from domain.attachments.attachment import Attachment
from typing import Optional, Callable
from infrastructure.orm.models.user_model import UserModel

class AttachmentMapper:
    @staticmethod
    def to_domain(model: AttachmentModel, user_loader: Optional[Callable[[str], object]] = None) -> Attachment:
        uploaded_by_domain = None
        if model.uploaded_by and user_loader:
            uploaded_by_domain = user_loader(str(model.uploaded_by.id))

        attachment = Attachment(
            filename=model.filename,
            uploaded_by=uploaded_by_domain,
            attachment_id=str(model.id)
        )
        attachment._uploaded_at = model.uploaded_at
        return attachment

    @staticmethod
    def to_orm(attachment: Attachment, model: Optional[AttachmentModel] = None) -> AttachmentModel:
        if model is None:
            model = AttachmentModel(id=attachment.get_id())
        model.filename = attachment.get_filename()
        # uploaded_by assignment must be done by caller
        return model
