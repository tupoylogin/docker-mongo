sh.enableSharding('taxi')
sh.shardCollection('taxi.rides', {start_latitude: "hashed"})