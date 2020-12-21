#!/bin/bash 

mongodb1=`getent hosts ${MONGO1} | awk '{ print $1 }'`
mongodb2=`getent hosts ${MONGO2} | awk '{ print $1 }'`
mongodb3=`getent hosts ${MONGO3} | awk '{ print $1 }'`

port=${PORT:-27017}

echo "Waiting for startup.."
echo "${MONGO_INITDB_ROOT_USERNAME}"

until mongo --host ${mongodb1}:${port} --eval 'quit(db.runCommand({ ping: 1 }).ok ? 0 : 2)' &>/dev/null; do
  printf '.'
  sleep 1
done

echo "Started.."

template='{"_id": "%s", "protocolVersion": 1, "members": [{"_id": 0,"host": "%s"},{"_id": 1,"host": "%s"},{"_id": 2,"host": "%s"}]}'
json_string=$(printf "${template}" "${RS}"  "${mongodb1}:${port}"  "${mongodb2}:${port}"  "${mongodb3}:${port}")


mongo --host ${mongodb1}:${port} --eval "rs.initiate($json_string);"

mongo --host ${mongodb1}:${port} <<EOF
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