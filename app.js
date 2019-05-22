'use strict'

var MongoClient = require('mongodb').MongoClient;

let atlas_connection_uri;
let cachedDb = null;

exports.handler = (event, context, callback) => {
    var uri = process.env['MONGODB_ATLAS_CLUSTER_URI'];
    
    if (atlas_connection_uri != null) {
        processEvent(event, context, callback);
    } 
    else {
        atlas_connection_uri = uri;
        console.log('the Atlas connection string is ' + atlas_connection_uri);
        processEvent(event, context, callback);
    } 
};

/*
// finished doc in the collection
{
  'metric': 'bob',
  'points': [
     { 'timestamp': 'abc', 'value': 50.5}
  ]
}
*/

function processEvent(event, context, callback) {
    console.log('Calling MongoDB Atlas from AWS Lambda with event: ' + JSON.stringify(event));
    var jsonContents = JSON.parse(JSON.stringify(event));
    
    context.callbackWaitsForEmptyEventLoop = false;
    
    try {
        if (cachedDb == null) {
            console.log('=> connecting to database');
            MongoClient.connect(atlas_connection_uri, { useNewUrlParser: true }, function (err, client) {
//console.log(err);
//console.log(client);
                cachedDb = client.db('metrics');
                return createDoc(cachedDb, jsonContents, callback);
            });
        }
        else {
            createDoc(cachedDb, jsonContents, callback);
        }
    }
    catch(err) {
        console.error('an error occurred', err);
    }
}

function createDoc(db, doc, callback) {
   //console.log(JSON.stringify(doc));
   db.collection('metrics').updateOne(
       { "metric": doc.metric },
       { $push: { "points": { "timestamp": new Date(), "value": doc.value } } },
       { upsert: true },
    function(err, result) {
      //console.log(result);
      if(err!=null) {
         console.error("an error occurred in createDoc", err);
         callback(null, JSON.stringify(err));
      }
      else {
         callback(null, "SUCCESS");
      }
   });
};

