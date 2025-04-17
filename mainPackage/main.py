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

if __name__ == "__main__":
    print("running")
    cleaner = dataclean("Data/fuelPurchaseData.csv")
    cleaner.clean()