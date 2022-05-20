from .recipe import Recipe
from application import db

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

    def isWordPresent(self, sentence, word):
     
        word = word.upper()
 
        # To convert the complete sentence in uppercase
        sentence = sentence.upper()
 
        # Both strings are converted to the same case,
        # so that the search is not case-sensitive
    
        # To break the sentence in words
        s = sentence.split()
    
        for temp in s :
    
            # Compare the current word
            # with the word to be searched
            if (temp == word) :
                return True
    
        return False
        
    def get_by_name(self, recipename):
        for recipe in self.recipes:
            if recipe.name in recipename:
                return recipe

    def get_by_keyword(self, keyword):
        found = []
        splitkeyword = keyword.split('_')
        
        #[found.append(recipe) if recipe.keyword.lower() in keyword.lower() else None for recipe in self.recipes]

        #[found.append(recipe) if recipe.name in keyword else None for recipe in self.recipes]

        for recipe in self.recipes:
            if (self.isWordPresent(recipe.keyword, splitkeyword[0])):
                found.append(recipe)
            elif recipe.keyword in keyword:
                found.append(recipe)

        return found

    def search_by_name(self, name):
        found = []
        splitname = name.split('_')
        
        #[found.append(recipe) if recipe.name.lower() in name.lower() else None for recipe in self.recipes]

        for recipe in self.recipes:
            if (self.isWordPresent(recipe.name, splitname[0])):
                found.append(recipe)
            elif recipe.name.lower() in name.lower():
                found.append(recipe)

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

    def test_clean(self):
        for elem in db.find({"name":"Recipe One"}):
            db.delete_one({"name":"Recipe One"})
        for elem in db.find({"name":"Recipe Two"}):
            db.delete_one({"name":"Recipe Two"})
    
    """def save(self):
        with open("data/data.json", "w") as fp:
            json.dump([rec.to_dict() for rec in self.recipes], fp)"""