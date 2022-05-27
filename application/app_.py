from flask import request, render_template, redirect, flash
from models.recipe import Recipe
from models.recipebook import RecipeBook
from application import app

collection = RecipeBook('collections')


''' Route to display the home page and search '''
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html", recipes=collection.recipes)
    if request.method == 'POST':
        search = request.form.get("Recipe Keyword")
        select = request.form.get('comp_select')
        if search != '':
            return redirect('/search/{}'.format(search+'_'+select))
        else:
            flash('No Recipes Found', 'error')
            return redirect('/')


''' Route to display search results '''
@app.route('/search/<recipe>')
def search(recipe):
    if 'keyword' in recipe:
        list_to_display = collection.get_by_keyword(recipe)
    elif 'name' in recipe:
        list_to_display = collection.search_by_name(recipe)
    else:
        list_to_display=False
    if list_to_display:
        return render_template("index.html", recipes=list_to_display)
    else:
        flash('No Recipes Found', 'error')
        return redirect('/')


''' Route to display a single recipe card '''
@app.route('/recipes/<recipe>', methods=['GET', 'DELETE'])
def display(recipe):
    if request.method == 'GET':
        recipes = []
        recipes.append(collection.get_by_name(recipe))
        recipes.append(collection.recipes)
        return render_template("displayrecipe.html", recipe=recipes)    

    if request.method == 'DELETE':
        collection.delete(recipe)
        return redirect('/')


''' Route to create a new recipe in the database '''
@app.route('/create_recipe.html', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create_recipe.html")

    if request.method == 'POST':
        instructions = str(request.form.get("Recipe Instructions"))
        ingredients = str(request.form.get("Recipe Ingredients"))
        keyword = str(request.form.get("Recipe Keyword"))
        name = str(request.form.get("Recipe Name"))
        if collection.get_by_name(name) is None:
                new_entry = Recipe(name, ingredients, instructions, keyword)
                collection.add(new_entry)
                return redirect('/recipes/{}'.format(name))
        flash('Recipe Name Exists', 'error')
        return redirect('/')


''' Route to update an existing recipe resource '''
@app.route('/update/<recipe>', methods=['GET', 'PUT'])
def update(recipe):
    if request.method  == 'GET':
        recipes = []
        recipes.append(collection.get_by_name(recipe))
        recipes.append(collection.recipes)
        return render_template("updaterecipe.html", recipe=recipes)

    if request.method == 'PUT':

        new_name = str(request.form.get("Recipe Name"))

        if (collection.get_by_name(new_name) is None) or (collection.get_by_name(new_name) == collection.get_by_name(recipe)):
            new_instructions = str(request.form.get("Recipe Instructions"))
            new_ingredients = str(request.form.get("Recipe Ingredients"))
            new_keyword = str(request.form.get("Recipe Keyword"))
            collection.update(recipe, new_name, new_keyword, new_ingredients, new_instructions)
            return redirect('/')
        flash("Recipe Name Exists", "error")
        return redirect('/')