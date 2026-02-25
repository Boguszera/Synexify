# infrastructure/repositories/comment_django_repository.py


from django.apps import apps
from django.db import transaction

from domain.comments.comment import Comment
from domain.repositories.comment_repository import CommentRepository
from infrastructure.orm.mappers.comment_mapper import CommentMapper


class CommentDjangoRepository(CommentRepository):
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_by_id(self, comment_id: str) -> Comment | None:
        CommentModel = apps.get_model("orm", "CommentModel")
        try:
            model = CommentModel.objects.select_related("author").get(id=comment_id)
        except CommentModel.DoesNotExist:
            return None

        author = self.user_repo.get_by_id(str(model.author_id)) if model.author_id else None
        return CommentMapper.to_domain(model, author=author)

    def save(self, comment: Comment, task_id: str) -> Comment:
        CommentModel = apps.get_model("orm", "CommentModel")
        with transaction.atomic():
            model_data = CommentMapper.to_orm(comment, task_id)
            orm_obj, _ = CommentModel.objects.update_or_create(
                id=model_data.id,
                defaults={
                    "content": model_data.content,
                    "task_id": model_data.task_id,
                    "author_id": model_data.author_id,
                },
            )
            model_data.created_at = orm_obj.created_at
        return self.get_by_id(comment.get_id())

    def delete(self, comment_id: str) -> None:
        CommentModel = apps.get_model("orm", "CommentModel")
        CommentModel.objects.filter(id=comment_id).delete()

    def list_by_task(self, task_id: str) -> list[Comment]:
        CommentModel = apps.get_model("orm", "CommentModel")
        models = CommentModel.objects.filter(task_id=task_id).order_by("created_at").select_related("author")
        result = []
        for m in models:
            author = self.user_repo.get_by_id(str(m.author_id)) if m.author_id else None
            result.append(CommentMapper.to_domain(m, author))
        return result
