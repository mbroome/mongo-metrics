import json
import time
import base64

from pymongo import MongoClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
client = MongoClient(os.environ['MONGODB_ATLAS_CLUSTER_URI'])

# Set database
db = client.metrics

def lambda_handler(event, context):
   logger.info("Received event: " + json.dumps(event, indent=2))

   collection = db.metrics
   pointData = json.loads(event)
   logger.info(json.dumps(pointData))

   response = collection.update_one(
                 { "metric": pointData['metric'] },
                 { "$push": { "points": { "timestamp": time.time(), "value": pointData['value'] } } },
                 { "upsert": True })

   return json.loads(json.dumps(response, default=json_unknown_type_handler))

def json_unknown_type_handler(x):
    """
    JSON cannot serialize decimal, datetime and ObjectId. So we provide this handler.
    """
    if isinstance(x, bson.ObjectId):
        return str(x)
    raise TypeError("Unknown datetime type")

