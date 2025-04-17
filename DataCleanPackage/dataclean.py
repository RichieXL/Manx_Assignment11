# File Name : dataclean.py
# Student Name: Dylan Sams, Richie James, Saivamsi Reddy Amireddy
# email:  samsds@mail.uc.edu, amiredsr@mail.uc.edu, james2c4@mail.uc.edu 
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment: This assignment is about cleaning up the data in a .csv file 

# Brief Description of what this module does. This module instantiates the class dataClean. This class removes any duplicate rows and sets all rows in gross price to have 2 decimal places.
# Citations: ChatGPT: https://chatgpt.com/c/680028dd-c3a4-800b-a347-6a2372dc86e3

# Anything else that's relevant:

import pandas as pd
import os

class dataclean:
    """
    A utility class for cleaning transaction data in a CSV file.
    """
    def __init__(self, input_file, output_folder='Data', output_file='cleanedData.csv'):
        """
        Initializes the cleaner with input and output file paths.
        @param input_file str: Path to the input CSV file.
        @param output_folder str: Directory where cleaned CSV will be saved.
        @param output_file str: Name of the cleaned CSV file.
        """
        self.input_file = input_file
        self.output_folder = output_folder
        self.output_file = os.path.join(output_folder, output_file)
        self.df = None

    def load_data(self):
        """
        Loads the CSV data into a DataFrame.
        """
        self.df = pd.read_csv(self.input_file, dtype={"Transaction Number": str})
        print("Data loaded successfully.")

    def format_gross_price(self):
        """
        Formats the 'Gross Price' column to 2 decimal places.
        """
        if 'Gross Price' in self.df.columns:
            self.df['Gross Price'] = self.df['Gross Price'].astype(float).map("{:.2f}".format)
            print("'Gross Price' formatted to 2 decimal places.")
        else:
            raise KeyError("'Gross Price' column not found in data.")

    def remove_duplicates(self):
        """
        Removes duplicate rows from the DataFrame.
        """
        before = len(self.df)
       
        self.df['Transaction Number'] = self.df['Transaction Number'].astype(str).str.strip()

        self.df = self.df.drop_duplicates(subset=['Transaction Number'], keep='first')
        
        after = len(self.df)
        print(f"Removed {before - after} duplicate rows.")

    def save_clean_data(self):
        """
        Saves the cleaned data to the output CSV file.
        """
        os.makedirs(self.output_folder, exist_ok=True)
        self.df.to_csv(self.output_file, index=False)
        print(f"Cleaned data saved to {self.output_file}")

    def clean(self):
        """
        Runs the full cleaning process in order.
        """
        self.load_data()
        self.format_gross_price()
        self.remove_duplicates()
        self.save_clean_data()
