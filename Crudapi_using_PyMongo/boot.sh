#!/bin/bash
set -e

printf "\n"
printf "****** Creating Network ******\n"
docker network create flask-mongo-network;
printf "****** Network Created ******\n"

printf "\n"

printf "****** Starting db_mongo Container ******\n"
docker container run \
    --detach \
    --name=db_mongo \
    --env MONGO_INITDB_ROOT_USERNAME=$MONGO_USERNAME \
    --env MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASSWORD \
    --net flask-mongo-network \
    mongo;
printf "****** db_mongo Container Started ******\n"

printf "\n"

printf "****** Creating api_flask Image ******\n"
docker image build . --tag api_flask;
printf "****** api_flask Image Created ******\n"

printf "\n" 

printf "****** Starting api_flask Container ******\n"
docker container run \
    --detach \
    --name=api_flask \
    --publish=8010:5000 \
    --net flask-mongo-network \
    api_flask;
printf "****** api_flask Container Started ******\n"

printf "\n"

printf "****** All Containers are Up and Running ******"

printf "\n"