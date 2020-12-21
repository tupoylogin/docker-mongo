taxi = db.getSiblingDB('taxi');

DBQuery.shellBatchSize = 100;

agg_base = taxi.rides.aggregate([
                    { '$match': {'driver_rate':{'$ne':null}}},
                    { '$group': { '_id': "$driver_id", 'driver_avg_rate': { '$avg': "$driver_rate" },  'start_avg_time': { '$avg': "$start_time" }} },
                    { '$sort': { 'driver_avg_rate': -1 } },
                    { '$limit' : 50 },
                    { '$match': {'start_avg_time': {"$lt": 12}}}
                   ])