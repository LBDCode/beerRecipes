import uuid
from src.models.recipe import Recipe
import datetime
from src.common.database import Database


class Style(object):
    def __init__(self, style, description, _id=None):
        self.style = style
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_style(self, style, description):
        recipe = Recipe(style_id=self._id,
                    style=style,
                    description=description)
        recipe.save_recipe()

    def get_recipes(self):
        return Recipe.from_style(self._id)

    def save_to_mongo(self):
        Database.insert(collection="styles",
                        data=self.json())

    def json(self):
        return {
            "style": self.style,
            "description": self.description,
            "_id": self._id
        }

    @classmethod
    def from_mongo(cls, id):
        style_data = Database.find_one(collection="styles", query={"_id": id})

        return cls(**style_data)

