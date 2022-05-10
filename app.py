from flask import Flask, request, json, url_for, render_template, redirect, flash
from models.recipe import Recipe
from models.recipebook import RecipeBook
import os
app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
filename = os.path.join(SITE_ROOT,'data','data.json')


collection = RecipeBook('collections')

def writeJSON():
    with open(filename,'w') as test_data:
            data = []
            for i in collection.recipes:
                data.append(i.__dict__)
            json.dump(data, test_data,
                        indent=4,  
                        separators=(',',': '))
   
@app.route('/')
def home():
    print(collection.recipes)
    return render_template("index.html",recipes=collection.recipes)

@app.route('/recipes/<recipe>',methods=['GET','DELETE'])
def display(recipe):
    if request.method == 'GET':
        return render_template("displayrecipe.html", recipe =  collection.get_by_name(recipe))    

    if request.method == 'DELETE':
        collection.delete(recipe)
        writeJSON()
        return redirect('/')

@app.route('/create_recipe.html',methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template("create_recipe.html")

    if request.method == 'POST':
        print(request.get_data())
        instructions = str(request.form.getlist("Recipe Instructions")[0])
        ingredients = str(request.form.getlist("Recipe Ingredients")[0])
        name = str(request.form.getlist("Recipe Name")[0])
        for i in collection.recipes:
            if name == i.name:
                flash('Recipe Name Already Exists','error')
                return redirect('/')
        new_entry = Recipe(name,ingredients,instructions)
        collection.add(new_entry)
        writeJSON()
        return redirect('/')

@app.route('/update/<recipe>',methods=['GET','PUT'])
def update(recipe):
    if request.method  == 'GET':
        return render_template("updaterecipe.html", recipe = collection.get_by_name(recipe))

    if request.method == 'PUT':
        collection.get_by_name(recipe).instructions = str(request.form.getlist("Recipe Instructions")[0])
        collection.get_by_name(recipe).ingredients = str(request.form.getlist("Recipe Ingredients")[0])
        collection.get_by_name(recipe).name = str(request.form.getlist("Recipe Name")[0])
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

