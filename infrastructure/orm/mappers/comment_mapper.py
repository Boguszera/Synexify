# infrastructure/orm/mappers/comment_mapper.py
from infrastructure.orm.models.comment_model import CommentModel
from domain.comments.comment import Comment
from typing import Optional, Callable
from domain.users.user_base import UserBase
from infrastructure.orm.models.user_model import UserModel

class CommentMapper:
    @staticmethod
    def to_domain(model: CommentModel, user_loader: Optional[Callable[[str], UserBase]] = None) -> Comment:
        author_domain = None
        if model.author and user_loader:
            author_domain = user_loader(str(model.author.id))

        comment = Comment(
            content=model.content,
            author=author_domain,
            comment_id=str(model.id)
        )
        comment._created_at = model.created_at
        return comment

    @staticmethod
    def to_orm(comment: Comment, model: Optional[CommentModel] = None) -> CommentModel:
        if model is None:
            model = CommentModel(id=comment.get_id())
        model.content = comment.get_content()
        # author assignment must be done by caller
        return model
