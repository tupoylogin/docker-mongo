rs.initiate(
    {
        "_id": "cnf-serv", 
        "configsvr": true,
        "protocolVersion": 1, 
        "members": [
            {
                "_id": 0,
                "host": "mongo-cfg-1:27017",
                "priority": 2
            },
            {
                "_id": 1,
                "host": "mongo-cfg-2:27017"
            },
            {
                "_id": 2,
                "host": "mongo-cfg-3:27017"
            }
        ]
    }
);