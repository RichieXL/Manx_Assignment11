# File Name : dataclean.py
# Student Name: Dylan Sams, Richie James, Saivamsi Reddy Amireddy
# email:  samsds@mail.uc.edu, amiredsr@mail.uc.edu, james2c4@mail.uc.edu 
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment: This assignment is about cleaning up the data in a .csv file 

# Brief Description of what this module does. This module instantiates the class dataClean. This class removes any duplicate rows and sets all rows in gross price to have 2 decimal places.
# Citations: https://chatgpt.com/c/680028dd-c3a4-800b-a347-6a2372dc86e3

# Anything else that's relevant:

import pandas as pd
import os

class FuelDataCleaner:
    def __init__(self, input_path, cleaned_path = "Data", anomalies_path='dataAnomalies.csv'):
        """
        Initializes removing and adding rows into a new csv file.
        @param input_path: str: Path to the input CSV file.
        @param cleaned_path: where data will be moved to
        @param anomalies_path: where unnesesary data will be place ina csv
        """
        self.input_path = input_path
        self.cleaned_path = cleaned_path
        self.anomalies_path = anomalies_path
        self.df = pd.read_csv(input_path)

    def load_data(self):
        self.df = pd.read_csv(self.input_path, dtype={"Transaction Number": str})
        print("Data loaded successfully.")

    def remove_pepsi(self):
        """Removes rows where 'pepsi' (case-insensitive) is found in the 'Fuel Type' column."""
        initial_rows = len(self.df)
        pepsi_rows = self.df[self.df['Fuel Type'].str.lower().str.contains('pepsi')]
        self.df = self.df[~self.df['Fuel Type'].str.lower().str.contains('pepsi')].copy()
        removed_rows = len(pepsi_rows)
        if removed_rows > 0:
            print(f"[FuelDataCleaner] Removed {removed_rows} rows containing 'pepsi' in 'Fuel Type'.")
        else:
            print("[FuelDataCleaner] No rows found with 'pepsi' in 'Fuel Type'.")

    def extract_anomalies(self):
        anomalies = self.df[self.df['Fuel Type'].str.lower() == 'pepsi'].copy()
        if not os.path.exists('Data'):
            os.makedirs('Data')
        anomalies.to_csv(self.anomalies_path, index=False)
        print(f"[FuelDataCleaner] Anomalies (Fuel Type 'pepsi') extracted to: {self.anomalies_path}")
        self.df = self.df[self.df['Fuel Type'].str.lower() != 'pepsi'].copy()

    def save_clean_data(self):
        if not os.path.exists(os.path.dirname(self.cleaned_path)):
            os.makedirs(os.path.dirname(self.cleaned_path))
        self.df.to_csv(self.cleaned_path, index=False)
        print(f"[FuelDataCleaner] Cleaned data (excluding anomalies) saved to: {self.cleaned_path}")

    def process(self):
        """
        Runs the process in a specific order
        """
        self.load_data()
        self.extract_anomalies()
        self.remove_pepsi()
        self.save_clean_data()