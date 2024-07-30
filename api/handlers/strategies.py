from pymongo import MongoClient
import json
import logging
from environs import Env

env = Env()
env.read_env()

MONGO_USER = env('MONGO_USER', 'pygit')
MONGO_PASSWORD = env('MONGO_PASSWORD', 'sesame')
MONGO_DATABASE = env('MONGO_DATABASE', 'tradetracker')
MONGO_APPNAME = env('MONGO_APPNAME', 'trader')
MONGO_HOSTNAME = env('MONGO_HOSTNAME', 'localhost')
MONGO_PORT = env('MONGO_PORT', 55000)

# logging setup
FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format=FORMAT,level=logging.INFO)

collection = 'strategies'
db = 'trades'

logging.info("Establishing client for monogdb...")

client = MongoClient('localhost', 55000)

logging.info(f"Using collection {collection} in database {db} for strategies...")
db = client[db]
collection = db[collection]

def get_all_strategies():
    result = []
    for r in collection.find():
        r['_id'] = str(r['_id'])
        result.append(r)
    return result

def get_strategy(strategy):
    result = []
    for r in collection.find({'name': strategy}, {"name": 1, "description": 1, "links": 1}):
        r['_id'] = str(r['_id'])
        result.append(r)
    return result

def create_strategy(strategy):
    record = {
        'name': strategy.name,
        'description': strategy.description,
        'links': [
            strategy.links
        ]
    }

    logging.info(f"Updating record {json.dumps(record)}")

    result = collection.update_one(
        {'name': record['name']}, {"$set": record}, upsert=True
    )

    logging.info(f"Inserted document with _id {result.upserted_id}")

    return { 'status': result.acknowledged }
