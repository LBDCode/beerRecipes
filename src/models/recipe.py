import uuid
from src.common.database import Database
import datetime
from bson.objectid import ObjectId


# name, style ID, IBU, yield, description, ingredients, instructions

class Recipe(object):

    def __init__(self, style_id, name, ibu, yld, description, ingredients, instructions, _id=None):
        self.style_id = style_id
        self.name = name
        self.ibu = ibu
        self.yld = yld
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_recipe(self):
        Database.insert(collection="reciepes",
                        data=self.recipe_info())

    def recipe_info(self):
        return {
            '_id': self._id,
            'style_id': self.style_id,
            'name': self.name,
            'ibu': self.ibu,
            'yld': self.yld,
            'description': self.description,
            'ingredients': self.ingredients,
            'instructions': self.instructions
        }



    @classmethod
    def findAll_mongo(cls):
        recipes = Database.find(collection='recipes', query={})

        return [cls(**recipe) for recipe in recipes]


    @classmethod
    def from_mongo(cls, id):
        recipe_data = Database.find_one(collection='recipes', query={"_id": ObjectId(id)})


        return cls(**recipe_data)

    @staticmethod
    def from_style(id):
        return [recipe for recipe in Database.find(collection='recipes', query={'style_id': id})]