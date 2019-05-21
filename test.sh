P="XXXXXXXXX"
export MONGODB_ATLAS_CLUSTER_URI='mongodb://metrics:${P}@freemetrics-shard-00-00-ekt2m.mongodb.net:27017,freemetrics-shard-00-01-ekt2m.mongodb.net:27017,freemetrics-shard-00-02-ekt2m.mongodb.net:27017/test?ssl=true&replicaSet=freemetrics-shard-0&authSource=admin&retryWrites=true'

node_modules/lambda-local/bin/lambda-local/lambda-local -l app.js -e event.json
