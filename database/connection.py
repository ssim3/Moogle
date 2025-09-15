import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")

client = pymongo.MongoClient(DB_URI)
db = client[DB_NAME]
