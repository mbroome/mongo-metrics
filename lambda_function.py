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

def lambda_handler(event, context):
   data = {}
   logger.info("Received event: " + json.dumps(event, indent=2))
   if 'body' in event:
      data = json.loads(event['body'])
   else:
      data = event
      
   collection = db.metrics
   logger.info(json.dumps(data))

   response = collection.update_one(
                 { "metric": data['metric'] },
                 { "$push": { "points": { "$each": [{ "timestamp": datetime.datetime.utcnow(), "value": data['value'] }], "$slice": -864 } }  },
                 True)

   return(True)

