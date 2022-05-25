from bson.objectid import ObjectId

from .recipe import Recipe
from application import db

class RecipeBook:
    """The RecipeBook Class"""

    def __init__(self, name):
        """the main attributes of a recipe are initialized here: name"""

        if type(name) != str:
            raise ValueError
        else:
            self.name = name

            self.recipes = [
                Recipe(
                    elem["name"],
                    elem["ingredients"],
                    elem["instructions"],
                    elem["keyword"]
                )for elem in db.find()
            ]

    def isWordPresent(self, sentence, word):
        """checks if the word is present in the sentence and returns a boolean"""

        word = word.upper()
        sentence = sentence.upper()
        s = sentence.split()
    
        for temp in s :
            if (temp == word) :
                return True
    
        return False
        
    def get_by_name(self, recipename):
        """returns a single recipe based on the given recipe name"""

        for recipe in self.recipes:
            if recipe.name in recipename:
                return recipe

    def get_by_keyword(self, keyword):
        """returns a list of recipes that match the given keyword"""

        found = []
        splitkeyword = keyword.split('_')
        
        for recipe in self.recipes:
            if (self.isWordPresent(recipe.keyword, splitkeyword[0])):
                found.append(recipe)
            elif recipe.keyword in keyword:
                found.append(recipe)

        return found

    def search_by_name(self, name):
        """returns a list of recipes that match the given recipe name"""

        found = []
        splitname = name.split('_')
    
        for recipe in self.recipes:
            if (self.isWordPresent(recipe.name, splitname[0])):
                found.append(recipe)
            elif recipe.name.lower() in name.lower():
                found.append(recipe)

        return found

    def __len__(self):
        """returns the number of recipes in the collection"""

        return len(self.recipes)

    def add(self, instance):
        """adds a recipe to the database as a dict"""

        if type(instance) is not Recipe:
            raise TypeError
        
        self.recipes.append(instance)
        db.insert_one(instance.to_dict())

    def delete(self, recipename):
        """deletes a recipe from the database"""

        rec = self.get_by_name(recipename)
        if rec:
            self.recipes.remove(rec)
            db.delete_one({"name":rec.name})
            return True
        
        return False

    def test_clean(self):
        """test function that deletes test recipes"""

        for elem in db.find({"name":"Recipe One"}):
            db.delete_one({"name":"Recipe One"})
        for elem in db.find({"name":"Recipe Two"}):
            db.delete_one({"name":"Recipe Two"})
    
    def update(self, recipe, name, keyword, ingredients, instructions):
        """updates a recipe in the database with the new changes"""

        doc = db.find_one({"name":recipe})
        if doc:
            doc=doc['_id']
        self.get_by_name(recipe).instructions = instructions
        self.get_by_name(recipe).ingredients = ingredients
        self.get_by_name(recipe).keyword = keyword
        self.get_by_name(recipe).name = name
        new_entry = self.get_by_name(name)
        db.update_one({"_id":ObjectId(doc)},{
            "$set":{
                "name": new_entry.name,
                "ingredients": new_entry.ingredients,
                "instructions": new_entry.instructions,
                "keyword": new_entry.keyword
            }}
        )


    # def save(self):
    #     """saves a recipe to the JSON file"""
    #     with open("data/data.json", "w") as fp:
    #         json.dump([rec.to_dict() for rec in self.recipes], fp)