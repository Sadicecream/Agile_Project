class Recipe:
    """The Recipe Class"""

    def __init__(self, name: str, ingredients: str, instructions: str, keyword: str):
        """the main attributes of a recipe are initialized here: name, ingredients, instructions, and keywords"""
        
        if type(name) != str:
            raise ValueError
        else:
            self.name = name
        
        if type(ingredients) != str:
            raise ValueError
        else:
            self.ingredients = ingredients
        
        if type(instructions) != str:
            raise ValueError
        else:
            self.instructions = instructions

        if type(keyword) != str:
            raise ValueError
        else:
            self.keyword = keyword


    def to_dict(self):
        """returns the Recipe attributes as a dict"""
        return {attr: getattr(self, attr) for attr in ("name", "ingredients", "instructions", "keyword")}
