from flask import Flask, render_template, request, Response, session, make_response, jsonify
# from src.models.user import User
# from src.models.styles import Style
from src.models.recipe import Recipe
from src.common.database import Database
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__)
app.secret_key = "libby"

def to_json(data):
    return json.dumps(data, default=json_util.default)

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home_template():
    recipes = Recipe.findAll_mongo()
    return render_template('index.html', recipes=recipes)

# all recipes api
@app.route('/api/recipes')
def recipe_all():
    recipes = Recipe.findAll_mongo()
    json_results = []
    for recipe in recipes:
        json_results.append(recipe.recipe_info())
    return Response(to_json(json_results), content_type='application/json')

# specific recipe
@app.route('/recipe/<string:recipe_id>')
def recipe_one(recipe_id):
    recipe = Recipe.from_mongo(recipe_id)
    print(recipe._id, recipe.name)
    return render_template('recipe.html', recipe=recipe)

# edit specific recipe
@app.route('/recipes/edit/<string:_id>', methods=['POST', 'GET'])
def edit_recipe(_id):
    if request.method == 'GET':
        id = "ObjectId(" + '"' + _id + '")'
        recipe = Recipe.from_mongo(_id)
        print(recipe._id, recipe.name)
        return render_template('new_recipe.html')
    # else:
    #     recipe = request.json
    #     Database.insert(collection="recipes", data=recipe, id=id)
    #     print(recipe)
    #
    #     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# new recipe
@app.route('/recipes/new', methods=['POST', 'GET'])
def create_new_recipe():
    if request.method == 'GET':
        return render_template('new_recipe.html')
    else:
        recipe = request.json
        Database.insert(collection="recipes", data=recipe)
        print(recipe)

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# browse by style
@app.route('/browse')
def recipe_style():
    return render_template("recipes_grid.html")




if __name__ == '__main__':
    app.run()


# TODO
# browse recipes by type
# search for recipes
# user accounts
# edit and save recioe
# convert recipe
