#!/bin/bash

## Fake data
python faker.py data/london_postcodes-ons-postcodes-directory-MAY20.csv data/rides.csv --num_rows=10_000_000

## Start the whole stack
docker-compose up -d 

## Config servers setup
docker exec -it mongo-cfg-1 sh -c "mongo --port 27017 < /scripts/create-cnf-rs.js"

## Shard servers setup
docker exec -it mongo-1-1 sh -c "mongo --port 27017 < /scripts/create-rs.js" 

sleep 15

## Apply sharding configuration
docker exec -it mongo-router sh -c "mongo --port 27017 < /scripts/create-shard.js"

## Enable admin account
docker exec -it mongo-router sh -c "mongo --port 27017 < /scripts/create-global-admin.js"

## Create sharded collection and fill it with data
docker exec -it mongo-router sh -c "mongo < /scripts/create-shard-collection.js"
docker exec -it mongo-router sh -c "mongoimport --port 27017 -d taxi -c rides --type csv --file /data/rides.csv --headerline"
docker exec -it mongo-router sh -c "mongo < /scripts/crud-query.js"