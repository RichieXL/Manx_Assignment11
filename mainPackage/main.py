# File Name : dataclean.py
# Student Name: Dylan Sams, Richie James, Saivamsi Reddy Amireddy
# email:  samsds@mail.uc.edu, amiredsr@mail.uc.edu, james2c4@mail.uc.edu 
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment: This assignment is about cleaning up the data in a .csv file 

# Brief Description of what this module does. 
# Citations: 

# Anything else that's relevant:

from DataCleanPackage.dataclean import *
from AddressPackage.address import *

if __name__ == "__main__":
    print("running")
    cleaner = dataclean("Data/fuelPurchaseData.csv")
    cleaner.clean()

    # fb8b7760-1b3d-11f0-8785-f37e8f1e4284
    api_key = "fb8b7760-1b3d-11f0-8785-f37e8f1e4284"
    if api_key:
        try:
            zip_filler = ZipCodeFiller(cleaner.df, api_key)
            zip_filler.fill_missing_zip_codes()

            cleaner.save_clean_data()  # Save updated file
        except Exception as e:
            print(f"ZIP code update failed gracefully: {e}")
    else:
        print("API key not found. Skipping ZIP code enrichment.")

