#Fill in later
from unittest.mock import mock_open, patch
from urllib import response
import requests 
import pytest
from setup import app

FLASK_URL = "http://localhost:5000"
recipe = "muffins"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def get_url(endpoint):
    resp = requests.get(f"{FLASK_URL}/{endpoint}")
    return resp

def test_check_home(client):
    # See the recipe collection
    r1 = get_url("/")
    assert r1.status_code == 200
    assert "Recipes" in resp.text
    assert "Create New Recipe" in resp.text

    # Check a non existing collection
    r1 = get_url("/fhidsfs")
    assert r1.status_code == 404

    

'''def test_check_create_recipe():
    r2 = get_url("/create_recipe.html")
    assert r2.status_code == 200
    assert "Name" in r2.text
    assert "Ingredients" in r2.text
    assert "Instructions" in r2.text
    
def test_check_update_recipe():
    r3 = get_url("/update/{recipe}")
    assert r3.status_code == 200
    assert "Cancel" in r3.text
    assert "Save" in r3.text
    assert "Edit:" in r3.text

def test_check_display_recipe():
    r4 = get_url("/recipes/{recipe}")
    assert r4.status_code == 200
    assert "Ingredients" in r4.text 
    assert "Instructions" in r4.text'''

