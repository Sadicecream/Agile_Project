from unittest.mock import mock_open, patch

import pytest

from models.recipe import Recipe
from models.recipebook import RecipeBook

JSON_FILE = """[
    
    {"name": "Cake", "ingredients": "eggs, flour, milk", "instructions": "something", "keyword": "easy"}, 
    {"name": "Cupcakes", "ingredients": "eggs, milk", "instructions": "something", "keyword": "easy"}, 
    {"name": "Brownies", "ingredients": "sugar, flour", "instructions": "something", "keyword": "chocolate"}, 
    {"name": "Muffins", "ingredients": "eggs, milk", "instructions": "something123", "keyword": "breakfast"}

]"""

@pytest.fixture
@patch("builtins.open", new_callable=mock_open, read_data=JSON_FILE)
def recs(mock_file):
    return RecipeBook("Our Recipes")

@patch("builtins.open", new_callable=mock_open, read_data="[]")
def test_open(mock_file):
    recs = RecipeBook("Our Recipes")
    mock_file.assert_called_once()
    assert "data/data.json" in mock_file.call_args[0]

def test_attributes_recipebook(recs):
    assert recs.name == "Our Recipes"
    for i in recs.recipes:
        assert type(i) is Recipe
    assert len(recs) == 4

def test_attribute_errors():
    with pytest.raises(ValueError):
        RecipeBook(123)

def test_get_by_name(recs):
    muffin = recs.get_by_name("Muffins")
    assert muffin.name == "Muffins"
    assert muffin.ingredients == "eggs, milk"
    assert muffin.instructions == "something123"
    assert muffin.keyword == "breakfast"

def test_get_by_keyword(recs):
    result = recs.get_by_keyword("easy")
    assert len(result) == 2

def test_add_recipe(recs):
    cookies = Recipe(name="Cookies", ingredients="Sugar, Milk, Butter", instructions="something", keyword="fast")
    assert type(cookies) == Recipe
    recs.add(cookies)
    assert cookies in recs.recipes

def test_add_error(recs):
    cookies = RecipeBook('Cookies')
    with pytest.raises(TypeError):
        recs.add(cookies)

def test_delete_recipe(recs):
    result = recs.delete("Muffins")
    assert result is True

    for i in recs.recipes:
        assert i.name != "Muffins"

    result = recs.delete("Muffins")
    assert result is False

@patch("builtins.open", new_callable=mock_open)
def test_save(mock_file, recs):
    recs.save()
    mock_file.assert_called_once_with("data/data.json", "w")
