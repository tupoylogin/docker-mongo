#!/bin/bash 

mongodb1=`getent hosts ${MONGO1} | awk '{ print $1 }'`
mongodb2=`getent hosts ${MONGO2} | awk '{ print $1 }'`
mongodb3=`getent hosts ${MONGO3} | awk '{ print $1 }'`

port=${PORT:-27017}

template='{"_id": "%s", "configsvr": true, "protocolVersion": 1, "members": [{"_id": 0,"host": "%s"},{"_id": 1,"host": "%s"},{"_id": 2,"host": "%s"}]}'
json_string=$(printf "${template}" "${RS}"  "${mongodb1}:${port}"  "${mongodb2}:${port}"  "${mongodb3}:${port}")

echo "Waiting for startup.."
until mongo admin --host ${mongodb1}:${port} --eval 'quit(db.runCommand({ ping: 1 }).ok ? 0 : 2)' &>/dev/null; do
  printf '-'
  sleep 1
done
echo "Started.."

mongo admin --host ${mongodb1}:${port} --eval "rs.initiate($json_string)"

mongo admin --host ${mongodb1}:${port} < scripts/create-user-admin.js
mongo admin --host ${mongodb1}:${port} --eval "db.getSiblingDB('test').createUser({user: 'foo', pwd: 'bar'})"
