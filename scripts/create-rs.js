rs.initiate(
    {
        "_id": "rs1", 
        "protocolVersion": 1, 
        "members": [
            {
                "_id": 0,
                "host": "mongo-1-1:27017",
                "priority": 2
            },
            {
                "_id": 1,
                "host": "mongo-1-2:27017"
            },
            {
                "_id": 2,
                "host": "mongo-1-3:27017"
            }
        ]
    }
);