FROM mongo:latest

RUN apt-get update && apt-get -y install curl
RUN mongod --fork --logpath /var/log/mongod.log