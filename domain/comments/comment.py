# domain/comments/comment.py
class Comment:
    def __init__(self, content, author):
        self._content = content
        self._author = author

    def edit_content(self, new_content):
        self._content = new_content