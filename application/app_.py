from flask import Flask, request, render_template, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from requests import session
from models.recipe import Recipe, db
from models.recipebook import RecipeBook
from application import app

collection = RecipeBook('collections')

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html",recipes=collection.recipes)
    if request.method == 'POST':
        search = request.form.get("Recipe Keyword")
        select = request.form.get('comp_select')
        if search != '':
            return redirect('/search/{}'.format(search+'_'+select))
        else:
            flash('No Recipes Found','error')
            return redirect('/')

@app.route('/search/<recipe>')
def search(recipe):
    if 'keyword' in recipe:
        list_to_display = collection.get_by_keyword(recipe)
    elif 'name' in recipe:
        list_to_display = collection.search_by_name(recipe)
    else:
        list_to_display = False
    if list_to_display:
        return render_template("index.html", recipes = list_to_display)
    else:
        flash('No Recipes Found','error')
        return redirect('/')
    
@app.route('/recipes/<recipe>',methods=['GET','DELETE'])
def display(recipe):
    if request.method == 'GET':
        recipes = []
        recipes.append(collection.get_by_name(recipe))
        recipes.append(collection.recipes)
        return render_template("displayrecipe.html", recipe =  recipes)    

    if request.method == 'DELETE':
        collection.delete(recipe)
        return redirect('/')

@app.route('/create_recipe.html',methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template("create_recipe.html")

    if request.method == 'POST':
        instructions = str(request.form.get("Recipe Instructions"))
        ingredients = str(request.form.get("Recipe Ingredients"))
        keyword = str(request.form.get("Recipe Keyword"))
        name = str(request.form.get("Recipe Name"))
        if collection.get_by_name(name) == None:
                new_entry = Recipe(name,ingredients,instructions,keyword)
                collection.add(new_entry)
                return redirect('/recipes/{}'.format(name))
        flash('Recipe Name Exists','error')
        return redirect('/')

@app.route('/update/<recipe>',methods=['GET','PUT'])
def update(recipe):
    if request.method  == 'GET':
        recipes = []
        recipes.append(collection.get_by_name(recipe))
        recipes.append(collection.recipes)
        return render_template("updaterecipe.html", recipe = recipes)

    if request.method == 'PUT':
        doc = db.find_one({"name":recipe})
        if doc:
            doc=doc['_id']

        new_name = str(request.form.get("Recipe Name"))

        if (collection.get_by_name(new_name) == None) or (collection.get_by_name(new_name) == collection.get_by_name(recipe)):
            collection.get_by_name(recipe).instructions = str(request.form.get("Recipe Instructions"))
            collection.get_by_name(recipe).ingredients = str(request.form.get("Recipe Ingredients"))
            collection.get_by_name(recipe).keyword = str(request.form.get("Recipe Keyword"))
            collection.get_by_name(recipe).name = new_name
            new_entry = collection.get_by_name(new_name)
            db.update_one({"_id":ObjectId(doc)},{
                "$set":{
                    "name": new_entry.name,
                    "ingredients": new_entry.ingredients,
                    "instructions": new_entry.instructions,
                    "keyword": new_entry.keyword
                }}
            )
            return redirect('/')
        flash("Recipe Name Exists","error")
        return redirect('/')


