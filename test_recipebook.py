from unittest.mock import mock_open, patch

import pytest

from .models.recipe import Recipe
from .models.recipebook import RecipeBook
from __init__ import db
from .app import collection

JSON_FILE = """[
    
    {"name": "Cake", "ingredients": "eggs, flour, milk", "instructions": "something", "keyword": "easy"}, 
    {"name": "Cupcakes", "ingredients": "eggs, milk", "instructions": "something", "keyword": "easy"}, 
    {"name": "Brownies", "ingredients": "sugar, flour", "instructions": "something", "keyword": "chocolate"}

]"""

@pytest.fixture
@patch("builtins.open", new_callable=mock_open, read_data=JSON_FILE)
def recs(mock_file):
    return RecipeBook("Our Recipes")

# @patch("builtins.open", new_callable=mock_open, read_data="[]")
# def test_open(mock_file):
#     recs = RecipeBook("Our Recipes")
    #mock_file.assert_called_once()
    #assert "data/data.json" in mock_file.call_args[0]


def test_attributes_recipebook(recs):
    assert recs.name == "Our Recipes"
    for i in recs.recipes:
        assert type(i) is Recipe
    assert len(recs) == len(recs.recipes)

def test_attribute_errors():
    with pytest.raises(ValueError):
        RecipeBook(123)

def test_get_by_name(recs):
    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    
    pancakes = recs.get_by_name("Recipe One")
    
    assert pancakes.name == "Recipe One"
    assert pancakes.ingredients == "random ingredients"
    assert pancakes.instructions == "Combine something"
    assert pancakes.keyword == "random keyword"

    recs.delete("Recipe One")

def test_get_by_keyword(recs):
    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    recs.add(Recipe("Recipe Two", "random ingredients", "Combine something", "random keyword"))

    result = recs.get_by_keyword("random keyword")
    assert len(result) == 2
    result = recs.get_by_keyword("random")
    assert len(result) == 2

    recs.delete("Recipe One")
    recs.delete("Recipe Two")

def test_add_recipe(recs):
    cookies = Recipe(name="Cookies", ingredients="Sugar, Milk, Butter", instructions="something", keyword="fast")
    assert type(cookies) == Recipe
    recs.add(cookies)
    assert cookies in recs.recipes

    recs.delete(cookies.name)

def test_add_error(recs):
    cookies = RecipeBook('Cookies')
    with pytest.raises(TypeError):
        recs.add(cookies)

def test_delete_recipe(recs):
    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    result = recs.delete("Recipe One")
    assert result is True

    for i in recs.recipes:
        assert i.name != "Recipe One"

    result = recs.delete("Recipe One")
    assert result is False

def test_search_by_name(recs):
    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    recs.add(Recipe("Recipe Two", "random ingredients", "Combine something", "random keyword"))

    result = recs.search_by_name("Recipe One")
    assert len(result) == 1
    result = recs.search_by_name("Recipe")
    assert len(result) == 2

    recs.delete("Recipe One")
    recs.delete("Recipe Two")

def test_present_word(recs):
    assert recs.isWordPresent("Hello my name is", "name") == True


# @patch("builtins.open", new_callable=mock_open)
# def test_save(mock_file, recs):
#     recs.save()
#     mock_file.assert_called_once_with("data/data.json", "w")
