from unittest.mock import mock_open, patch
from urllib import response
import requests 
import pytest
from application import app, app_

FLASK_URL = "http://localhost:5000"
recipe = "muffins"

@pytest.fixture
def client():
    return app.test_client()

#gets the requested URL
def get_url(endpoint):
    resp = requests.get(f"{FLASK_URL}/{endpoint}")
    return resp

def test_check_home(client):
    #check if the homepage collection was returned

    r1 = client.get('/')
    assert r1.status_code == 200
    assert "Recipes" in r1.text
    assert "Create New Recipe" in r1.text

    #check a collection that doesn't exist
    r1 = client.get("/fhidsfs")
    assert r1.status_code == 404

    

def test_check_create_recipe(client):
    #checks if the create recipe page was returned

    r2 = client.get("/create_recipe.html")
    assert r2.status_code == 200
    assert "Name" in r2.text
    assert "Ingredients" in r2.text
    assert "Instructions" in r2.text
    
def test_check_update_recipe(client):
    #checks if the update recipe page was returned

    r3 = client.get("/update/{recipe}")
    assert r3.status_code == 200
    assert "Cancel" in r3.text
    assert "Save" in r3.text
    assert "Edit:" in r3.text

def test_check_display_recipe(client):
    #checks if the display recipes page was returned

    r4 = client.get("/recipes/{recipe}")
    assert r4.status_code == 200
    assert "Ingredients" in r4.text 
    assert "Instructions" in r4.text

