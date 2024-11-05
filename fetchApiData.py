import requests
import pandas as pd

# Define the API endpoint
API_URL = "https://data.cityofnewyork.us/resource/5uac-w243.json"

# Define the number of records to fetch (e.g., 10,000)
NUM_RECORDS = 10000


# Function to fetch data from the API
def fetch_crime_data(num_records):
    # Set parameters to limit the number of records returned
    params = {
        "$limit": num_records
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        return response.json()  # Return the JSON data if the request was successful
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []


# Fetch the crime data
crime_data = fetch_crime_data(NUM_RECORDS)

# Create a DataFrame
df = pd.DataFrame(crime_data)

print(df)
# Clean up the DataFrame if necessary
df.dropna(subset=['latitude', 'longitude', 'boro_nm', 'law_cat_cd'], inplace=True)  # Drop rows with missing values
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Save the DataFrame to CSV
df.to_csv("data/nyc_crime_data.csv", index=False)

print(f"Fetched and saved {len(df)} records from the NYC Open Data API.")
