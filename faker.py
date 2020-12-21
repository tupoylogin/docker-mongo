import argparse

import pandas as pd
import numpy as np

from geopy.distance import geodesic

def random_date_generator(start_date: str, range_in_days: int):
    days_to_add = np.arange(0, range_in_days*1440) #in minutes
    random_date = np.datetime64(start_date) + np.random.default_rng().choice(days_to_add)
    yield random_date

def calc_cost(start_time: pd.datetime, distance: float):
    cost = 2 + 0.15 * distance
    if (start_time.hour >= 8 and start_time.hour <= 9) or \
        (start_time.hour >= 18 and start_time.hour <= 19):
        cost *= 1.5
    if (start_time.hour >= 22 or start_time.hour <= 6):
        cost *= 1.3
    return cost

def calc_road_time(distance: float):
    return distance*np.abs(np.random.default_rng().normal(0.1, 0.01))

def read_prepare(path: str, num_records: int):
    df = pd.read_csv(path, delimiter=',')
    rides = pd.DataFrame(columns=['driver_id', 'client_id',\
                              'start', 'start_latitude', 'start_longtitude', \
                              'finish', 'finish_latitude', 'finish_longtitude', \
                              'distance', 'road_time', 'start_time', 'finish_time', 'cost', \
                              'driver_rate', 'category_driver_feedback', 'text_driver_feedback',\
                             'client_rate', 'category_client_feedback', 'text_client_feedback'])
    rides['driver_id'] = np.random.randint(low=0, high=4000, size=num_records)
    rides['client_id'] = np.random.randint(low=0, high=4000, size=num_records)
    rides[['start', 'start_latitude', 'start_longtitude']] = df[['Postcode', 'Latitude', 'Longitude']]\
                                                            .sample(n=num_records, replace=True)\
                                                                .reset_index(drop=True)
    rides[['finish', 'finish_latitude', 'finish_longtitude']] = df[['Postcode', 'Latitude', 'Longitude']]\
                                                            .sample(n=num_records, replace=True)\
                                                                .reset_index(drop=True)
    rides['start_time'] = pd.to_datetime(sorted(np.array([random_date_generator('2014-01-01', 800) for i in range(num_records)])))
    
    rides['distance'] = [geodesic((x1, y1), (x2, y2)).km for x1, y1, x2, y2 in zip(rides['start_latitude'], \
                                                                                              rides['start_longtitude'], \
                                                                                              rides['finish_latitude'], \
                                                                                              rides['finish_longtitude'])]
    rides['cost'] = [calc_cost(s, d) for s, d in zip(rides.start_time, rides.distance)]
    rides['cost'] = rides['cost'].round(2)
    rides['road_time'] = rides['distance'].map(calc_road_time)
    driver_rate_idx = np.random.randint(low=0, high=num_records, size=int(num_records*0.3))
    driver_rate_distribution_arr = np.random.multinomial(1, [0.2, 0.05, 0.1, 0.25, 0.4], size=int(num_records*0.3))
    rides['driver_rate'][driver_rate_idx] = np.where(driver_rate_distribution_arr == 1)[1] + 1
    driver_feedback_categories_good = ['great service', 'nice car', 'wonderful companion', 'neat and tidy', 'expert navigation', 'recommend']
    driver_feedback_categories_bad = ['awful service', 'bad car', 'unpleasant companion', 'dirty', 'non-expert navigation', 'not recommend']
    category_driver_good_feedback_idx = np.random.choice(rides[rides.driver_rate > 3].index, size=int(num_records*0.3*0.2))
    rides["category_driver_feedback"][category_driver_good_feedback_idx] = np.random.choice(driver_feedback_categories_good, size=int(num_records*0.3*0.2))

    category_driver_bad_feedback_idx = np.random.choice(rides[rides.driver_rate < 4].index, size=int(num_records*0.3*0.2))
    rides["category_driver_feedback"][category_driver_bad_feedback_idx] = np.random.choice(driver_feedback_categories_bad, size=int(num_records*0.3*0.2))
    text_good_feedback_driver_length = np.random.randint(low=0, high=7, size=int(num_records*0.3*0.2))
    text_good_feedback_driver_sample = [np.random.choice(driver_feedback_categories_good, i) for i in text_good_feedback_driver_length]
    rides['text_driver_feedback'][category_driver_good_feedback_idx] = text_good_feedback_driver_sample

    text_bad_feedback_driver_length = np.random.randint(low=0, high=7, size=int(num_records*0.3*0.2))
    text_bad_feedback_driver_sample = [np.random.choice(driver_feedback_categories_bad, i) for i in text_bad_feedback_driver_length]
    rides['text_driver_feedback'][category_driver_bad_feedback_idx] = text_bad_feedback_driver_sample

    client_rate_idx = np.random.randint(low=0, high=num_records, size=int(num_records*0.5))
    client_rate_distribution_arr = np.random.multinomial(1, [0.2, 0.05, 0.1, 0.25, 0.4], size=int(num_records*0.5))
    rides['client_rate'][client_rate_idx] = np.where(client_rate_distribution_arr == 1)[1] + 1

    client_feedback_categories_good = ['polite', 'pleasant', 'quiet', 'neat and tidy', 'recommend']
    client_feedback_categories_bad = ['unpolite', 'unpleasant', 'loud', 'dirty','not recommend']

    category_client_good_feedback_idx = np.random.choice(rides[rides.client_rate > 3].index, size=int(num_records*0.3*0.2))
    rides["category_client_feedback"][category_client_good_feedback_idx] = np.random.choice(client_feedback_categories_good, size=int(num_records*0.3*0.2))

    category_client_bad_feedback_idx = np.random.choice(rides[rides.client_rate < 4].index, size=int(num_records*0.3*0.2))
    rides["category_client_feedback"][category_client_bad_feedback_idx] = np.random.choice(client_feedback_categories_bad, size=int(num_records*0.3*0.2))

    text_good_feedback_client_length = np.random.randint(low=0, high=6, size=int(num_records*0.3*0.2))
    text_good_feedback_client_sample = [np.random.choice(client_feedback_categories_good, i) for i in text_good_feedback_client_length]
    rides['text_client_feedback'][category_client_good_feedback_idx] = text_good_feedback_client_sample

    text_bad_feedback_client_length = np.random.randint(low=0, high=6, size=int(num_records*0.3*0.2))
    text_bad_feedback_client_sample = [np.random.choice(client_feedback_categories_good, i) for i in text_bad_feedback_client_length]
    rides['text_client_feedback'][category_client_good_feedback_idx] = text_bad_feedback_client_sample

    return rides

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('input', action='store', dest='infile')
    parser.add_argument('output', action='store', dest='outfile')
    parser.add_argument('--num_rows', action='store', type=int, default=1_000_000, dest='nrows')

    args = parser.parse_args()

    read_prepare(args.infile, args.nrows).to_csv(args.outfile, chunksize=100_000)

    


    


