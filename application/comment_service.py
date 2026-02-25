# application/comment_service

from domain.comments.comment import Comment
from domain.exceptions.exceptions import PermissionDenied
from domain.users.user_base import UserBase


class CommentService:
    def __init__(self, auth_service, comment_repo, task_repo, user_repo):
        self.auth = auth_service
        self.comment_repo = comment_repo
        self.task_repo = task_repo
        self.user_repo = user_repo

    def add_comment(self, task_id: str, user: UserBase, content: str) -> Comment:
        comment = Comment(content=content, author=user)
        return self.comment_repo.save(comment, task_id)

    def update_comment(self, comment_id: str, user: UserBase, new_content: str) -> Comment:
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")

        task_id = comment.get_task_id()

        if comment.get_author_id() != user.get_id() and user.get_role() not in ["admin", "manager"]:
            raise PermissionDenied(user.get_id(), action="update_comment", resource=comment_id)

        comment.edit_content(new_content)
        return self.comment_repo.save(comment, task_id)

    def delete_comment(self, comment_id: str, user: UserBase) -> None:
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            return

        if comment.get_author_id() != user.get_id() and user.get_role() not in ["admin", "manager"]:
            raise PermissionDenied(user.get_id(), action="delete_comment", resource=comment_id)

        self.comment_repo.delete(comment_id)

    def list_comments_for_task(self, task_id: str, user: UserBase):
        return self.comment_repo.list_by_task(task_id)
