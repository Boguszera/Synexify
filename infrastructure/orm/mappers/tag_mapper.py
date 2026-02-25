from domain.tags.tag import Tag
from infrastructure.orm.models.tag_model import TagModel


class TagMapper:
    @staticmethod
    def to_domain(model: TagModel) -> Tag:
        return Tag(tag_id=str(model.id), name=model.name)

    @staticmethod
    def to_orm(domain: Tag, model: TagModel = None) -> TagModel:
        if model is None:
            model = TagModel()
        model.name = domain.get_name()
        return model
