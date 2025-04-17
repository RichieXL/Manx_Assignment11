# File Name : address.py
# Student Name: Dylan Sams, Richie James, Saivamsi Reddy Amireddy
# email:  samsds@mail.uc.edu, amiredsr@mail.uc.edu, james2c4@mail.uc.edu 
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment: This assignment is about cleaning up the data in a .csv file 

# Brief Description of what this module does. This module instantiates the class address. The class takes zip code data from an api and updates it to cleanedData.csv
# Citations: ChatGPT: https://chatgpt.com/c/680060a6-c1c4-8000-b6c6-55521b644b69
# API: https://app.zipcodebase.com/documentation

# Anything else that's relevant:

import requests
import re
import pandas as pd

class address:
    """
    Handles ZIP code augmentation for addresses missing ZIP codes in a DataFrame.
    """
    def __init__(self, df, api_key):
        """
        Initializes the Address object with a DataFrame and API key.

        @param df pandas.DataFrame: The DataFrame containing address data.
        @param api_key str: API key for the ZIP code lookup service.
        """
        self.df = df
        self.api_key = api_key

    def has_zip(self, address):
        """
        Checks whether a ZIP code is present in the given address.

        @param address: str: The address string to check.
        @return: bool: True if a 5-digit ZIP code is found, False otherwise.
        """
        return bool(re.search(r"\b\d{5}\b", str(address)))

    def extract_city_state(self, address):
        """
        Attempts to extract the city and 2-letter state code from the given address.

        @param address str: A full address string.
        @return tuple(str or None, str or None): Extracted city and state, or (None, None) if not found.
        """
        parts = str(address).split(',')
        city = parts[-2].strip() if len(parts) >= 2 else None
        state_match = re.search(r'\b[A-Z]{2}\b', parts[-1]) if len(parts) >= 1 else None
        state = state_match.group(0) if state_match else None
        return city, state

    def fill_missing_zip_codes(self):
        """
        Finds and fills ZIP codes for the first 5 addresses missing them.
        """
        processed = 0

        for idx, row in self.df.iterrows():
            if processed >= 10:
                break

            full_address = row.get("Full Address", "")
            if not self.has_zip(full_address):
                city, state = self.extract_city_state(full_address)
                if city and state:
                    zip_code = self.lookup_zip(city, state)
                    if zip_code:
                        updated_address = f"{full_address.strip()} {zip_code}"
                        self.df.at[idx, "Full Address"] = updated_address
                        print(f"ZIP {zip_code} added to {city}, {state}")
                    else:
                        print(f"ZIP not found for {city}, {state}")
                    processed += 1
                else:
                    print(f"Could not parse city/state from address: {full_address}")

    def lookup_zip(self, city, state):
        """
        Calls an external API to fetch a ZIP code for the given city and state.

        @param city str: City name to look up.
        @param state str: 2-letter state abbreviation.
        @return str or None: ZIP code if found, else None.
        """
        import requests
        url = "https://app.zipcodebase.com/api/v1/code/city"
    
        params = {
            "apikey": self.api_key.strip(),
            "city": city,
            "state_name": state,
            "country": "US",
            "limit": 1
        }
    
        try:
            response = requests.get(url, params=params)
            print(f"[DEBUG] {city}, {state} -> Status {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                results = data.get('results')

                if isinstance(results, list) and results:
                    return results[0].get('postal_code')
                else:
                    print(f"[DEBUG] No usable ZIP in results for {city}, {state}")
            else:
                print(f"API Error {response.status_code} for {city}, {state}")

        except Exception as e:
            print(f"Request failed for {city}, {state}: {e}")
        return None
