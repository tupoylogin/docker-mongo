#!/bin/bash 

mongodb1=`getent hosts ${MONGO1} | awk '{ print $1 }'`
mongodb2=`getent hosts ${MONGO2} | awk '{ print $1 }'`
mongodb3=`getent hosts ${MONGO3} | awk '{ print $1 }'`

port=${PORT:-27017}

echo "Waiting for startup.."
until mongo --host ${mongodb1}:${port} --eval 'quit(db.runCommand({ ping: 1 }).ok ? 0 : 2)' &>/dev/null; do
  printf '.'
  sleep 1
done

echo "Started.."

echo "${MONGO_INITDB_ROOT_USERNAME}"

mongo --host ${mongodb1}:${port} <<EOF
   use admin;
   var cfg = {
        "_id": "${RS}",
        "protocolVersion": 1,
        "members": [
            {
                "_id": 0,
                "host": "${mongodb1}:${port}"
                "priority": 2
            },
            {
                "_id": 1,
                "host": "${mongodb2}:${port}"
            },
            {
                "_id": 2,
                "host": "${mongodb3}:${port}"
            }
        ]
    };
    rs.initiate(cfg, { force: true });
EOF
#rs.reconfig(cfg, { force: true });
mongo -u ${MONGO_INITDB_ROOT_USERNAME} -p ${MONGO_INITDB_ROOT_USERNAME} --host ${mongodb1}:${port} <<EOF
    admin = db.getSiblingDB("admin");
    admin.createUser(
    {
        user: "clRoot",
        pwd: "clRoot",
        roles: [
      { role: "clusterAdmin", db: "admin" },
      { role: "userAdmin", db: "admin" }
        ]
    }
    );
EOF
mongo -u ${MONGO_INITDB_ROOT_USERNAME} -p ${MONGO_INITDB_ROOT_USERNAME} --eval 'use test;'
mongoimport --type csv -d test -c postcodes_nov_14 --headerline --file ./data/London_postcode-ONS-postcode-Directory-Nov14.csv