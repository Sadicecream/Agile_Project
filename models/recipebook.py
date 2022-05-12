from models.recipe import Recipe
from __init__ import db

class RecipeBook:
    def __init__(self, name):
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


    
    def get_by_name(self, recipename):
        for recipe in self.recipes:
            if recipe.name == recipename:
                return recipe

    def get_by_keyword(self, keyword):
        found = []
        
        [found.append(recipe) if recipe.keyword in keyword else None for recipe in self.recipes]

        return found

    def __len__(self):
        return len(self.recipes)

    def add(self, instance):
        if type(instance) is not Recipe:
            raise TypeError
        
        self.recipes.append(instance)
        db.insert_one(instance.to_dict())

    def delete(self, recipename):
        rec = self.get_by_name(recipename)
        if rec:
            self.recipes.remove(rec)
            db.delete_one({"name":rec.name})
            return True
        
        return False
    
    """def save(self):
        with open("data/data.json", "w") as fp:
            json.dump([rec.to_dict() for rec in self.recipes], fp)"""