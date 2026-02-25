from domain.comments.comment import Comment
from domain.users.user_base import UserBase
from infrastructure.orm.models.comment_model import CommentModel


class CommentMapper:
    @staticmethod
    def to_domain(model: CommentModel, author: UserBase | None) -> Comment:
        comment = Comment(content=model.content, author=author, comment_id=str(model.id))
        if model.created_at:
            comment.set_created_at(model.created_at)

        if model.task_id:
            comment._task_id = str(model.task_id)

        return comment

    @staticmethod
    def to_orm(comment: Comment, task_id: str) -> CommentModel:
        model = CommentModel(id=comment.get_id(), content=comment.get_content(), task_id=task_id)
        if comment.get_author_id():
            model.author_id = comment.get_author_id()

        if comment.get_created_at():
            model.created_at = comment.get_created_at()
        return model
