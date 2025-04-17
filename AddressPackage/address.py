



import requests
import re
import pandas as pd

class ZipCodeFiller:
    def __init__(self, df, api_key):
        self.df = df
        self.api_key = api_key

    def has_zip(self, address):
        return bool(re.search(r"\b\d{5}\b", str(address)))

    def extract_city_state(self, address):
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
