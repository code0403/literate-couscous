# backend/database.py
from pymongo import MongoClient

def get_mongo_connection():
    # Replace 'your_mongodb_uri' with your MongoDB connection string
    client = MongoClient('mongodb://localhost:27017')
    return client['task_management_db']  # Replace 'task_management_db' with your desired database name
