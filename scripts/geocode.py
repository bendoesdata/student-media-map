import os
import json
import gspread
import pandas as pd
import googlemaps
from datetime import datetime

# --- Configuration ---
# Replace with your Google Sheet details
SPREADSHEET_ID = '1Z3waYLZ4eJXs_byDoRHVsh41-NCOTyEJL_KjceSuaSA'
WORKSHEET_NAME = 'Main Student Media List'
# Replace with your Google Maps API Key
GOOGLE_MAPS_API_KEY = 'AIzaSyBJXTdd_d_5BfopaF2p_o1XjVlEPaVoTnw'
# Path to your local credentials file
# CREDENTIALS_FILE = 'ccn-geocode-credentials.json'
# The path to your Vue app's public directory
CSV_OUTPUT_PATH = 'public/outlets.csv' 

# --- Setup ---
try:
    # This is the crucial line: accessing the environment variable
    credentials_json = os.environ.get('GOOGLE_CREDENTIALS') 
    if not credentials_json:
        raise ValueError("GOOGLE_CREDENTIALS environment variable not set.")
    
    creds = json.loads(credentials_json)
    gc = gspread.service_account_from_dict(creds)

    # this was for local testing, not GH action
    # print("Attempting to authenticate with Google Sheets...")
    # gc = gspread.service_account(filename=CREDENTIALS_FILE)
    # print("Successfully authenticated with Google Sheets.")

    # Authenticate with Google Maps Geocoding API
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    
except Exception as e:
    print(f"Error during setup: {e}")
    exit()

# --- Functions ---
def geocode_university(university_name):
    """Geocodes a university name using the Google Maps Geocoding API."""
    try:
        geocode_result = gmaps.geocode(f"{university_name}, USA")
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
    except Exception as e:
        print(f"Error geocoding {university_name}: {e}")
    return None, None

# def main():
#     """Main function to pull, geocode, and save data."""
#     try:
#         # Open the Google Sheet and read data
#         sh = gc.open_by_key(SPREADSHEET_ID)
#         worksheet = sh.worksheet(WORKSHEET_NAME)
#         data = worksheet.get_all_records()
#         df = pd.DataFrame(data)

#         print(f"Found {len(df)} records in the spreadsheet.")

#         # Geocode universities that don't have LAT/LONG
#         for index, row in df.iterrows():
#             if not row.get('LAT') or not row.get('LONG'):
#                 university = row.get('College/University')
#                 if university:
#                     print(f"Geocoding: {university}")
#                     # The error is likely here
#                     lat, lon = geocode_university(university)
#                     if lat and lon:
#                         df.at[index, 'LAT'] = lat
#                         df.at[index, 'LONG'] = lon
#                         print(f"  -> Found coordinates: {lat}, {lon}")
        
#         # Write back to sheet and save to CSV
#         worksheet.clear()
#         worksheet.update([df.columns.values.tolist()] + df.values.tolist())
#         print("Spreadsheet updated successfully.")
#         df.to_csv('outlets.csv', index=False)
#         print("Data saved to outlets.csv")

#     except Exception as e:
#         # This new block will catch errors during the main geocoding and data manipulation process
#         print(f"An error occurred during processing: {e}")

def main():
    """Main function to pull, geocode, and save data."""
    try:
        # Initial authentication check as before
        print("Attempting to authenticate with Google Sheets...")
        gc = gspread.service_account(filename=CREDENTIALS_FILE)
        print("Successfully authenticated with Google Sheets.")

        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    except Exception as e:
        print(f"Error during setup: {e}")
        exit()

    # The main processing logic is in a new try block for better error handling
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(WORKSHEET_NAME)
        
        # Get all values as a list of lists (more resilient than get_all_records)
        all_values = worksheet.get_all_values()
        print(all_values)
        # Check for empty sheet
        if not all_values:
            print("Spreadsheet is empty. No data to process.")
            return

        # Use the first row as the header
        headers = all_values[0]
        records = all_values[1:]

        # Create DataFrame from the list of lists
        df = pd.DataFrame(records, columns=headers)
        
        # Now, you can perform the geocoding logic
        print(f"Found {len(df)} records in the spreadsheet.")

        for index, row in df.iterrows():
            if not row.get('LAT') or not row.get('LONG'):
                university = row.get('College/University')
                if university:
                    print(f"Geocoding: {university}")
                    lat, lon = geocode_university(university)
                    if lat and lon:
                        df.at[index, 'LAT'] = lat
                        df.at[index, 'LONG'] = lon
                        print(f"  -> Found coordinates: {lat}, {lon}")

        # Write the updated data back to the Google Sheet
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("Spreadsheet updated successfully.")

        # Save the final DataFrame to the specified CSV path
        df.to_csv(CSV_OUTPUT_PATH, index=False)
        print(f"Data saved to {CSV_OUTPUT_PATH}")

    except Exception as e:
        import traceback
        print(f"An error occurred during processing: {e}")
        traceback.print_exc()
        
if __name__ == "__main__":
    main()
