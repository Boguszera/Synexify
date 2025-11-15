# domain/attachments/attachment.py
class Attachment:
    def __init__(self, filename, uploaded_by):
        self._filename = filename
        self._uploaded_by = uploaded_by

    def download(self):
        pass

    def delete(self):
        pass