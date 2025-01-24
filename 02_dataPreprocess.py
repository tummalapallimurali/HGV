# %% 
import pandas as pd
import numpy as np
import json
import os
import logging

'''Objective: Process the generated JSON files and produce analytical results while handling data efficiently.
Steps:
Data Processing:
Load all generated JSON files.
Process each flight record while identifying and cleaning "dirty" records (i.e., records with NULLvalues).
Result Output:
Total count of records processed.
Total count of "dirty" records.
Total runtime of the analysis phase in milliseconds.
Key Metrics:
Calculate the AVG (average) and P95 (95th percentile) of flight_duration_secs for the Top 25 destination cities by the total number of passengers arriving.
Passenger Balance Analysis:
Assume all cities initially have 0 passengers.
For each city, calculate the number of passengers remaining after accounting for departures and arrivals from all processed flight data.
Identify:
The city with the maximum remaining passengers.
The city with the minimum remaining passengers.'''

class preprocess():
    def __init__(self):
        # read all the files in the directory
        self.dir = './tmp/flights'
        # create a dataframe with column names and their data types
        self.data = pd.DataFrame(columns=['date', 'origin_city', 'destination_city', 'flight_duration_secs', '#_of_passengers_on_board'], dtype='object')
        # read all the files in the directory and store in a dataframe
        # log start time
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        
    def data_preprocess(self):
        logging.info('**Data Preprocessing Initated**')
        self.start_time = pd.Timestamp.now()
        for file in os.listdir(self.dir):
            with open(os.path.join(self.dir, file), 'r') as f:
                json_data = json.load(f)
                self.data = pd.concat([self.data, pd.DataFrame(json_data)])
        logging.info(f'Total number of records read: {self.data.shape[0]}')
        logging.info(f'Number of records with NULL values: {self.data.isnull().sum()}')
        self.data = self.data.dropna()
        self.end_time = pd.Timestamp.now()
        logging.info(f'Total runtime of the data cleaning phase in milliseconds: {self.end_time - self.start_time}')
        logging.info('**Data Preprocessing Completed**')
        return self.data
    
    def key_metrics(self):
        logging.info('**Key Metrics Calculation Started**')
        # logging.info(f'AVG flight_duration_secs for the Top 25 destination cities by the total number of passengers arriving: {self.data.groupby("destination_city")["flight_duration_secs"].mean().nlargest(25)}')
        # logging.info(f'P95 flight_duration_secs for the Top 25 destination cities by the total number of passengers arriving: {self.data.groupby("destination_city")["flight_duration_secs"].apply(lambda x: np.percentile(x, 95)).nlargest(25)}')
        self.data['flight_duration_secs'] = pd.to_numeric(self.data['flight_duration_secs'], errors='coerce')
        
        # Drop rows with NaN values in 'flight_duration_secs'
        self.data = self.data.dropna(subset=['flight_duration_secs'])

        # Group by 'destination_city' and calculate the mean of 'flight_duration_secs'
        top_25_destinations = self.data.groupby("destination_city")["flight_duration_secs"].mean().nlargest(25)

        logging.info(f'AVG flight_duration_secs for the Top 25 destination cities by the total number of passengers arriving: {top_25_destinations}')
        logging.info('**Key Metrics Calculation Completed**')
        return top_25_destinations

    def passenger_balance_analysis(self):
        logging.info('**Passenger Balance Analysis Initiated**')
        passenger_balance = pd.DataFrame(columns=['city', 'passengers'], dtype='int')
        passenger_balance['city'] = self.data['destination_city']
        passenger_balance['passengers'] = self.data['#_of_passengers_on_board']
        passenger_balance = passenger_balance.groupby('city').sum()
        passenger_balance['passengers'] = passenger_balance['passengers'] - self.data.groupby('origin_city')['#_of_passengers_on_board'].sum()
        logging.info(f'City with the maximum remaining passengers: {passenger_balance["passengers"].idxmax()}')
        logging.info(f'City with the minimum remaining passengers: {passenger_balance["passengers"].idxmin()}')
        logging.info('**Passenger Balance Analysis Completed**')
        return passenger_balance
    
    # collect all the loggings and update readme file
    def report(self):
        with open("README.md", "a") as f:
            f.write(f'\n\n{pd.Timestamp.now()}:\n')
            with open('preprocess.log', 'r') as log:
                f.write(log.read())
        logging.info('Report Updated')
        

    def run(self):
        self.data_preprocess()
        self.key_metrics()
        self.passenger_balance_analysis()
        self.report()

    

if __name__=='__main__':
    logging.basicConfig(filename='preprocess.log', level=logging.INFO)
    preprocess().run()




# %%
