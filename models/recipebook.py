from models.recipe import Recipe
import json

class RecipeBook:
    def __init__(self, name):
        if type(name) != str:
            raise ValueError
        else:
            self.name = name

        with open('data/data.json') as fp:
                self.recipes = [
                    Recipe(
                        elem["name"],
                        elem["ingredients"],
                        elem["instructions"],
                        elem["keyword"]
                    )for elem in json.load(fp)
                ]
    
    def get_by_name(self, recipename):
        for recipe in self.recipes:
            if recipe.name == recipename:
                return recipe

    def get_by_keyword(self, keyword):
        found = []
        
        [found.append(recipe) if recipe.keyword == keyword else None for recipe in self.recipes]

        return found

    def __len__(self):
        return len(self.recipes)

    def add(self, instance):
        if type(instance) is not Recipe:
            raise TypeError
        
        self.recipes.append(instance)

    def delete(self, recipename):
        rec = self.get_by_name(recipename)
        if rec:
            self.recipes.remove(rec)
            return True
        
        return False
    
    def save(self):
        with open("data/data.json", "w") as fp:
            json.dump([rec.to_dict() for rec in self.recipes], fp)