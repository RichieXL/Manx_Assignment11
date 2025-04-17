# File Name : data.py
# Student Name: Dylan Sams, Richie James, Saivamsi Reddy Amireddy
# email:  samsds@mail.uc.edu, amiredsr@mail.uc.edu, james2c4@mail.uc.edu 
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment: This assignment is about cleaning up the data in a .csv file 

# Brief Description of what this module does. This module instantiates the class data. The class checks for anomalies within the data and moves them to dataAnomalies.csv. 
# Citations: Gemini: https://gemini.google.com/app/1930a7a08f2bdf56

# Anything else that's relevant:

import pandas as pd
import os

class data:
    """
     A class to process a fuel transaction CSV file by
    """
    def __init__(self, input_path, cleaned_path = "Data/cleanedData.csv", anomalies_path='Data/dataAnomalies.csv'):
        """
        Initializes removing and adding rows into a new csv file.
        @param input_path str: Path to the input CSV file.
        @param cleaned_path str: where data will be moved to
        @param anomalies_path str: where unnesesary data will be place ina csv
        """
        self.input_path = input_path
        self.cleaned_path = cleaned_path
        self.anomalies_path = anomalies_path
        self.df = pd.read_csv(input_path)

    def load_data(self):
        """
        Loads the input CSV file into a pandas DataFrame
        """
        self.df = pd.read_csv(self.input_path, dtype={"Transaction Number": str})
        print("Data loaded successfully.")

    def remove_pepsi(self):
        """
        Removes rows where 'pepsi' (case-insensitive) is found in the 'Fuel Type' column.
        """
        initial_rows = len(self.df)
        pepsi_rows = self.df[self.df['Fuel Type'].str.lower().str.contains('pepsi')]
        self.df = self.df[~self.df['Fuel Type'].str.lower().str.contains('pepsi')].copy()
        removed_rows = len(pepsi_rows)
        if removed_rows > 0:
            print(f"[FuelDataCleaner] Removed {removed_rows} rows containing 'pepsi' in 'Fuel Type'.")
        else:
            print("[FuelDataCleaner] No rows found with 'pepsi' in 'Fuel Type'.")

    def extract_anomalies(self):
        """
        Extracts all rows containing 'pepsi' in the 'Fuel Type' column and writes them to a separate CSV file.
        """
        anomalies = self.df[self.df['Fuel Type'].str.lower().str.contains('pepsi', na=False)].copy()

        anomalies_dir = os.path.dirname(self.anomalies_path)
        if anomalies_dir and not os.path.exists(anomalies_dir):
            os.makedirs(anomalies_dir, exist_ok=True)

        anomalies.to_csv(self.anomalies_path, index=False)
        print(f"[FuelDataCleaner] Anomalies (Fuel Type contains 'pepsi') extracted to: {self.anomalies_path}")

        self.df = self.df[~self.df['Fuel Type'].str.lower().str.contains('pepsi', na=False)].copy()

    def save_clean_data(self):
        """
        Saves the cleaned DataFrame (with 'pepsi' rows removed) to the specified output CSV path.
        """
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
