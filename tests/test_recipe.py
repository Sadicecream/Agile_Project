import pytest
from models.recipe import Recipe

def test_attributes():
    """checks the main attributes of a recipe in the Recipe class"""

    muffin = Recipe("Muffins", "Eggs, Milk, Sugar", "instructions", "fast")
    assert muffin.name == "Muffins"
    assert muffin.ingredients == "Eggs, Milk, Sugar"
    assert muffin.instructions == "instructions"
    assert muffin.keyword == "fast"

def test_recipe_to_dict():
    """checks the dictionary method in the Recipe class"""

    muffin = Recipe("Muffins", "Eggs, Milk, Sugar", "instructions", "fast")
    assert muffin.to_dict() == {"name": "Muffins", "ingredients": "Eggs, Milk, Sugar", "instructions": "instructions", "keyword": "fast"}

def test_attribute_errors():
    """checks the main attribute errors in the Recipe class"""

    with pytest.raises(ValueError):
        Recipe(name=123, ingredients="Eggs, Milk, Sugar", instructions="instructions", keyword="fast")

    with pytest.raises(ValueError):
        Recipe(name="Recipe One", ingredients=1234, instructions="instructions", keyword="fast")

    with pytest.raises(ValueError):
        Recipe(name="Muffins", ingredients="Eggs, Milk, Sugar", instructions=123, keyword="fast")

    with pytest.raises(ValueError):
        Recipe(name="Muffins", ingredients="Eggs, Milk, Sugar", instructions="instructions", keyword=2233)

    with pytest.raises(ValueError):
        Recipe(name=244, ingredients=123, instructions=12334, keyword=123)