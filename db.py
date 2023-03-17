from flask_pymongo import pymongo
from app import app
import urllib.parse

password = urllib.parse.quote_plus('Jaheim2003@')
CONNECTION_STRING = "mongodb+srv://Jaheim:%s@cluster0.swcjr6y.mongodb.net/?retryWrites=true&w=majority"% password
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')