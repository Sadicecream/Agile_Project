from flask import Flask, request, render_template, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from models.recipe import Recipe
from models.recipebook import RecipeBook
from  __init__ import app ,db

#FETCH api
collection = RecipeBook('collections')

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html",recipes=collection.recipes)
    if request.method == 'POST':
        search = request.form.getlist("Recipe Keyword")[0]
        if search != '':
            return redirect('/search/{}'.format(search))
        else:
            flash('No Recipes Found','error')
            return redirect('/')

@app.route('/search/<recipe>')
def search(recipe):
    list_to_display = collection.get_by_keyword(recipe)
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
        print(recipes)
        return render_template("displayrecipe.html", recipe =  recipes)    

    if request.method == 'DELETE':
        collection.delete(recipe)
        return redirect('/')

@app.route('/create_recipe.html',methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template("create_recipe.html")

    if request.method == 'POST':
        instructions = str(request.form.getlist("Recipe Instructions")[0])
        ingredients = str(request.form.getlist("Recipe Ingredients")[0])
        keyword = str(request.form.getlist("Recipe Keyword")[0])
        name = str(request.form.getlist("Recipe Name")[0])
        print(collection.get_by_name(name))
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
        print(recipes)
        return render_template("updaterecipe.html", recipe = recipes)

    if request.method == 'PUT':
        doc = db.find_one({"name":recipe})['_id']
        print(request.form)

        new_name = str(request.form.getlist("Recipe Name")[0])

        if (collection.get_by_name(new_name) == None) or (collection.get_by_name(new_name) == collection.get_by_name(recipe)):
            collection.get_by_name(recipe).instructions = str(request.form.getlist("Recipe Instructions")[0])
            collection.get_by_name(recipe).ingredients = str(request.form.getlist("Recipe Ingredients")[0])
            collection.get_by_name(recipe).keyword = str(request.form.getlist("Recipe Keyword")[0])
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

if __name__ == "__main__":
    app.run(debug=True)

