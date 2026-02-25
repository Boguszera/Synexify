from domain.attachments.attachment import Attachment
from infrastructure.orm.models.attachment_model import AttachmentModel


class AttachmentMapper:
    @staticmethod
    def to_domain(model: AttachmentModel) -> Attachment:
        attachment = Attachment(filename=model.filename, uploaded_by=None, attachment_id=str(model.id))
        if model.uploaded_by_id:
            attachment.set_uploaded_by_id(str(model.uploaded_by_id))
        if model.uploaded_at:
            attachment.set_uploaded_at(model.uploaded_at)
        if model.task_id:
            attachment._task_id = str(model.task_id)

        return attachment

    @staticmethod
    def to_orm(attachment: Attachment, task_id: str) -> AttachmentModel:
        model = AttachmentModel(id=attachment.get_id(), filename=attachment.get_filename(), task_id=task_id)
        if attachment.get_uploaded_by_id():
            model.uploaded_by_id = attachment.get_uploaded_by_id()
        else:
            raise ValueError("Uploaded_by_id is required for ORM persistence")

        if attachment.get_uploaded_at():
            model.uploaded_at = attachment.get_uploaded_at()
        return model
