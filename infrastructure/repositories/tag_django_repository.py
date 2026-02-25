from django.apps import apps

from domain.tags.tag import Tag
from infrastructure.orm.mappers.tag_mapper import TagMapper


class TagDjangoRepository:
    def get_by_id(self, tag_id: str) -> Tag | None:
        TagModel = apps.get_model("orm", "TagModel")
        try:
            model = TagModel.objects.get(id=tag_id)
            return TagMapper.to_domain(model)
        except TagModel.DoesNotExist:
            return None

    def list_all(self) -> list[Tag]:
        TagModel = apps.get_model("orm", "TagModel")
        return [TagMapper.to_domain(m) for m in TagModel.objects.all()]

    def save(self, tag: Tag) -> Tag:
        TagModel = apps.get_model("orm", "TagModel")
        model = TagModel.objects.filter(id=tag.get_id()).first()
        model = TagMapper.to_orm(tag, model)
        model.save()
        return self.get_by_id(str(model.id))

    def delete(self, tag_id: str):
        TagModel = apps.get_model("orm", "TagModel")
        TagModel.objects.filter(id=tag_id).delete()
