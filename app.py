from flask import Flask, request, json, url_for, render_template, redirect
import os
app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
filename = os.path.join(SITE_ROOT,'data','data.json')
   
@app.route('/')
def home():
    if request.method == 'GET':
        with open(filename,'r') as test_data:
            data =json.load(test_data)

        return render_template("index.html",recipes=data)

@app.route('/recipes/<recipe>',methods=['GET','DELETE'])
def display(recipe):
    if request.method == 'GET':
        with open(filename,'r') as test_data:
            data =json.load(test_data)
            for i in data:
                if i["name"] == recipe:
                    recipe_to_display = i
                    return render_template("displayrecipe.html", display = recipe_to_display)
            return redirect('/')

    if request.method == 'DELETE':
        with open(filename,'r') as test_data:
            data =json.load(test_data)
            for i in data:
                if i["name"] == recipe:
                    data.remove(i)
        with open(filename,'w') as test_data:
            json.dump(data, test_data,
                        indent=4,  
                        separators=(',',': '))
        return redirect('/')

@app.route('/create_recipe.html',methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template("create_recipe.html")

    if request.method == 'POST':
        print(request.form)
        new_entry = {
            "instructions": str(request.form.getlist("Recipe Ingredients")[0]),
            "ingredients": str(request.form.getlist("Recipe Ingredients")[0]),
            "name": str(request.form.getlist("Recipe Name")[0])
            }
        with open(filename,'r') as test_data:
            data = json.load(test_data)
        data.append(new_entry)
        with open(filename, 'w') as test_data:
            json.dump(data, test_data,
                        indent=4,  
                        separators=(',',': '))
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

