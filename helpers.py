import pyodbc
import pandas as pd
import requests
from urllib.parse import urlencode

def get_new_access_token(client_id, client_secret):

    # Set the Strava API URLs
    authorization_url = 'https://www.strava.com/api/v3/oauth/authorize'
    token_url = 'https://www.strava.com/api/v3/oauth/token'

    # Define the redirect URI (should match what you've registered in your Strava application settings)
    redirect_uri = 'https://developers.strava.com/'  # Replace with your actual redirect URI

    # Step 1: Generate the authorization URL
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'activity:read_all',  # Adjust the scope as needed
    }

    authorization_url_with_params = authorization_url + '?' + urlencode(params)

    print(f'Visit this URL to authorize the application: {authorization_url_with_params}')
    authorization_code = input('Enter the authorization code from the callback URL: ')

    # Step 2: Exchange the authorization code for an access token and refresh token
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
    }

    response = requests.post(token_url, data=token_data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        refresh_token = token_info['refresh_token']  # Get the refresh token
        print(f'Success! Access Token: {access_token}')
        print(f'Refresh Token: {refresh_token}')
        return access_token, refresh_token
    else:
        print(f'Error: Unable to retrieve access token. Status code: {response.status_code}')
        print(response.json())




def get_request_from_strava_api(url, access_token):
    headers = {
        'accept': 'application/json',
        'authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
        
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the error response
        return {}


def upsert_dataframe_to_sql(dataframe, connection_string, table_name):
    try:
        # Establish a connection to the SQL Server
        conn = pyodbc.connect(connection_string)
        
        # Create a cursor object
        cursor = conn.cursor()

        # Create a staging table with the same structure as the target table
        staging_table_name = f"{table_name}_staging"
        cursor.execute(f"CREATE TABLE {staging_table_name} (LIKE {table_name})")

        # Bulk insert the data from the DataFrame into the staging table
        dataframe.to_sql(staging_table_name, conn, if_exists='replace', index=False)

        # Use the MERGE statement to upsert data from the staging table into the target table
        merge_query = f"""
            MERGE INTO {table_name} AS Target
            USING {staging_table_name} AS Source
            ON Target.id = Source.id
            WHEN MATCHED THEN
                UPDATE SET
                    Target.name = Source.name,
                    Target.activity_id = Source.activity_id,
                    -- Update other columns as needed
            WHEN NOT MATCHED THEN
                INSERT (id, name, activity_id, activity_type, distance, average_grade, maximum_grade, elevation_high, elevation_low, elevation_profile, climb_category, city, state, country, start_latitude, start_longitude, end_latitude, end_longitude)
                VALUES (Source.id, Source.name, Source.activity_id, Source.activity_type, Source.distance, Source.average_grade, Source.maximum_grade, Source.elevation_high, Source.elevation_low, Source.elevation_profile, Source.climb_category, Source.city, Source.state, Source.country, Source.start_latitude, Source.start_longitude, Source.end_latitude, Source.end_longitude);
        """
        cursor.execute(merge_query)
        conn.commit()

        print("Upsert operation completed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up: Drop the staging table
        cursor.execute(f"DROP TABLE {staging_table_name}")
        conn.commit()
        conn.close()


