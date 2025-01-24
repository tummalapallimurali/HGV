# %%
import json
import os
import pandas as pd
import numpy as np
import argparse

# %%
'''This class is responsible for generating flight data in JSON format'''

class DataPrep:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Generate flight data.')
        parser.add_argument('--cities_pool', nargs='+', default=['NewYork', 'LosAngeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'SanAntonio', 'SanDiego', 'Dallas', 'SanJose'], help='List of cities to use as the pool of origin and destination cities.')
        parser.add_argument('--dirty_records_prob', type=float, default=0.01, help='Probability of generating dirty records with NULL values.')
        parser.add_argument('--num_files', type=int, default=5, help='Number of files to generate.')
        parser.add_argument('--num_records_range', nargs=2, type=int, default=[50, 100], help='Range of number of records per file.')

        args = parser.parse_args()

        self.cities_pool = args.cities_pool
        self.dirty_records_prob = args.dirty_records_prob
        self.num_files = args.num_files
        self.num_records_range = args.num_records_range
        self.dir = './tmp/flights'

    def generate_flight_data(self):
        for i in range(self.num_files):
            num_records = np.random.randint(self.num_records_range[0], self.num_records_range[1])
            flights = []
            for j in range(num_records):
                flight = {}
                flight['date'] = pd.Timestamp.now().date().isoformat()
                flight['origin_city'] = np.random.choice(self.cities_pool)
                flight['destination_city'] = np.random.choice(self.cities_pool)
                flight['flight_duration_secs'] = np.random.randint(3600, 7200)
                flight['#_of_passengers_on_board'] = np.random.randint(50, 200)
                if np.random.rand() < self.dirty_records_prob:
                    flight['origin_city'] = None
                flights.append(flight)
            
            # create a folder if it does not exist
            file_name = f"{pd.Timestamp.now().strftime('%m-%y')}-{np.random.choice(self.cities_pool)}-flights.json"

            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            file_name = os.path.join(self.dir, file_name)

            with open(file_name, 'w') as f:
                json.dump(flights, f)
            print(f'File {file_name} created with {num_records} records')

# if main
if __name__=='__main__':
    dp = DataPrep()
    dp.generate_flight_data()