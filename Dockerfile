FROM mongo:4.0.1

RUN apt-get update && apt-get -y install curl