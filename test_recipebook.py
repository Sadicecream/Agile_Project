from unittest.mock import mock_open, patch

import pytest

from models.recipe import Recipe
from models.recipebook import RecipeBook

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
    """checks the main attributes of a recipebook in the RecipeBook class"""

    assert recs.name == "Our Recipes"
    for i in recs.recipes:
        assert type(i) is Recipe
    assert len(recs) == len(recs.recipes)

def test_attribute_errors():
    """checks the main attribute errors in the RecipeBook class"""

    with pytest.raises(ValueError):
        RecipeBook(123)

def test_get_by_name(recs):
    """checks the get by name method that returns a single recipe based on recipe name"""

    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    
    pancakes = recs.get_by_name("Recipe One")
    
    assert pancakes.name == "Recipe One"
    assert pancakes.ingredients == "random ingredients"
    assert pancakes.instructions == "Combine something"
    assert pancakes.keyword == "random keyword"

    recs.delete("Recipe One")
    recs.test_clean()

def test_get_by_keyword(recs):
    """checks the get by keyword method that returns a list based on given keyword"""

    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    recs.add(Recipe("Recipe Two", "random ingredients", "Combine something", "random keyword"))

    result = recs.get_by_keyword("random keyword")
    assert len(result) == 2
    result = recs.get_by_keyword("random")
    assert len(result) == 2

    recs.delete("Recipe One")
    recs.delete("Recipe Two")
    recs.test_clean()

def test_add_recipe(recs):
    """checks the add recipe method that adds a recipe to the database"""

    cookies = Recipe(name="Cookies", ingredients="Sugar, Milk, Butter", instructions="something", keyword="fast")
    assert type(cookies) == Recipe
    recs.add(cookies)
    assert cookies in recs.recipes

    recs.delete(cookies.name)
    recs.test_clean()

def test_add_error(recs):
    """checks the add recipe errors"""

    cookies = RecipeBook('Cookies')
    with pytest.raises(TypeError):
        recs.add(cookies)

def test_delete_recipe(recs):
    """checks the delete recipe method that deletes a recipe from the database"""

    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    result = recs.delete("Recipe One")
    assert result is True

    for i in recs.recipes:
        assert i.name != "Recipe One"

    result = recs.delete("Recipe One")
    assert result is False
    recs.test_clean()

def test_search_by_name(recs):
    """checks the search by name method that returns a list of recipes based on recipe name"""

    recs.add(Recipe("Recipe One", "random ingredients", "Combine something", "random keyword"))
    recs.add(Recipe("Recipe Two", "random ingredients", "Combine something", "random keyword"))

    result = recs.search_by_name("Recipe One")
    assert len(result) == 1
    result = recs.search_by_name("Recipe")
    assert len(result) == 2

    recs.delete("Recipe One")
    recs.delete("Recipe Two")
    recs.test_clean()

def test_present_word(recs):
    """checks the present word function that returns a boolean if the word is in the sentence"""

    recs.test_clean()
    assert recs.isWordPresent("Hello my name is", "name") == True


# @patch("builtins.open", new_callable=mock_open)
# def test_save(mock_file, recs):
#     recs.save()
#     mock_file.assert_called_once_with("data/data.json", "w")
