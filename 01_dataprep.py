# %%
import json
import os
import pandas as pd
import numpy as np

# %%
'''Folder Structure: Files should be stored in a directory like /tmp/flights/%MM-YY%-%origin_city%-flights.json, where:
%MM-YY% corresponds to the current month and year.
%origin_city% is the name of the origin city.
File Contents:
Each file should be a JSON array of flight records.
Randomly generate the number of records per file, M, within the range [50 – 100].
Flight Data Fields: Each flight record should contain the following:
date: The date of the flight in ISO format (YYYY-MM-DD).
origin_city: The name of the city where the flight originated.
destination_city: The name of the city where the flight arrived.
flight_duration_secs: Total duration of the flight in seconds.
#_of_passengers_on_board: Number of passengers onboard.
Cities Pool: Randomly select cities from a set of K = [100-200] city names.
Dirty Records: With a probability L = [0.5% - 1%], some flight records should have NULL values in one or more fields.'''

class DataPrep:
    def __init__(self, cities_pool, dirty_records_prob):
        self.cities_pool = cities_pool
        self.dirty_records_prob = dirty_records_prob
        self.dir = './tmp/flights'

    def generate_flight_data(self, num_files, num_records_range):
        for i in range(num_files):
            num_records = np.random.randint(num_records_range[0], num_records_range[1])
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

# %%
if __name__=='__main__':
    cities_pool = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    dirty_records_prob = 0.01
    num_files = 5
    dp = DataPrep(cities_pool, dirty_records_prob)
    dp.generate_flight_data(num_files, [50, 100])


# %%
