from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET"
app.config['MONGO_URI'] = "mongodb+srv://agile_user:ACIT2911@2911-cluster.qasof.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db.ACIT.AGILE