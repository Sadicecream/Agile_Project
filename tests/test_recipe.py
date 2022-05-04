import pytest
from models.recipe import Recipe

def test_attributes():
    muffin = Recipe("Muffins", "Eggs, Milk, Sugar", "instructions")
    assert muffin.name == "Muffins"
    assert muffin.ingredients == "Eggs, Milk, Sugar"
    assert muffin.instructions == "instructions"

def test_recipe_to_dict():
    muffin = Recipe("Muffins", "Eggs, Milk, Sugar", "instructions")
    assert muffin.to_dict() == {"name": "Muffins", "ingredients": "Eggs, Milk, Sugar", "instructions": "instructions"}

def test_attribute_errors():
    with pytest.raises(ValueError):
        Recipe(name=123, ingredients="Eggs, Milk, Sugar", instructions="instructions")

    with pytest.raises(ValueError):
        Recipe(name="Muffins", ingredients=1234, instructions="instructions")

    with pytest.raises(ValueError):
        Recipe(name="Muffins", ingredients="Eggs, Milk, Sugar", instructions=123)

    with pytest.raises(ValueError):
        Recipe(name=244, ingredients=123, instructions=12334)