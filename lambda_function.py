import os
import logging
import json
import bson
import datetime
import base64

from pymongo import MongoClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set client
client = MongoClient(os.environ['MONGODB_ATLAS_CLUSTER_URI'])

# Set database
db = client.metrics

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

def lambda_handler(event, context):
   logger.info("Received event: " + json.dumps(event, indent=2))

   collection = db.metrics
   logger.info(json.dumps(event))

   response = collection.update_one(
                 { "metric": event['metric'] },
                 { "$push": { "points": { "timestamp": datetime.datetime.utcnow(), "value": event['value'] } } },
                 True)

   #return json.loads(json.dumps(response, cls=DateTimeEncoder))
   return(True)
      
