import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
mongo = os.getenv("MONGO")
client = pymongo.MongoClient(mongo)
db = client["bot"]
welcome = db["welcome"]