from helpers import *
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

# Replace these values with your actual Strava application's credentials
client_id = os.environ.get('strava_client_id')
client_secret = os.environ.get('strava_client_secret')
mssqlusername = os.environ.get('mssqlusername')
mssqlserver = os.environ.get('mssqlservere')
mssqldatabase = os.environ.get('mssqldatabase')
mssqlpassword = os.environ.get('mssqlpassword')
refresh_token = "2847793802330d53b1cbe3a91e878da7f756dfbd"
access_token = '403f8cd119afb0ea3c1ae44504e730d7852154fc'
#access_token, new_refresh_token = get_new_access_token(client_id, client_secret)
activities_list_url = 'https://www.strava.com/api/v3/athlete/activities?per_page=200'

activities_df = get_request_from_strava_api(activities_list_url, access_token)
activities_df = pd.DataFrame(activities_df)
activities_df = activities_df[['id', 'type', 'distance', 'moving_time', 'elapsed_time', 'total_elevation_gain', 
                'start_date_local', 'start_latlng', 'end_latlng', 'average_speed', 'max_speed',
                'average_heartrate', 'max_heartrate', 'elev_high', 'elev_low']]

activities_df['start_latitude'] = activities_df.start_latlng.apply(lambda x: x[0] if x != [] else np.nan)
activities_df['start_longitude'] = activities_df.start_latlng.apply(lambda x: x[1] if x != [] else np.nan)
activities_df['end_latitude'] = activities_df.end_latlng.apply(lambda x: x[0] if x != [] else np.nan)
activities_df['end_longitude'] = activities_df.end_latlng.apply(lambda x: x[1] if x != [] else np.nan)
print(activities_df.columns)
activities_df = activities_df.drop(['start_latlng', 'end_latlng'], axis=1)
print(activities_df)
activities_df.to_csv('df.csv')

activity_id = '9743724307'
activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
segments_df = get_request_from_strava_api(activity_url, access_token)

segments_df = pd.DataFrame(segments_df['segment_efforts'])
segments_df['activity_id'] = activity_id

single_segment_df = pd.DataFrame(list(segments_df.segment))

segments_df = segments_df[['id', 'name', 'activity_id', 'elapsed_time', 'moving_time', 
                           'start_date_local', 'distance', 'start_index', 'end_index',	
                           'average_heartrate', 'max_heartrate']]

single_segment_df['start_latitude'] = single_segment_df.start_latlng.apply(lambda x: x[0] if x != [] else np.nan)
single_segment_df['start_longitude'] = single_segment_df.start_latlng.apply(lambda x: x[1] if x != [] else np.nan)
single_segment_df['end_latitude'] = single_segment_df.end_latlng.apply(lambda x: x[0] if x != [] else np.nan)
single_segment_df['end_longitude'] = single_segment_df.end_latlng.apply(lambda x: x[1] if x != [] else np.nan)
single_segment_df['activity_id'] = activity_id
single_segment_df = single_segment_df[['id', 'name', 'activity_id', 'activity_type', 'distance', 
                                       'average_grade' ,'maximum_grade', 'elevation_high', 
                                       'elevation_low', 'elevation_profile', 'climb_category',
                                       'city', 'state', 'country', 'start_latitude', 'start_longitude',
                                       'end_latitude', 'end_longitude'

]]

print(segments_df)
segments_df.to_csv('seg.csv')
print(single_segment_df)
single_segment_df.to_csv('single_seg.csv')

# Example usage:
# Assuming you have a DataFrame 'df' containing your data
# Set your SQL Server connection string
connection_string = "DRIVER={ODBC Driver 18 for SQL Server};" + f"SERVER={mssqlserver};DATABASE={mssqldatabase};UID={mssqlusername};PWD={mssqlpassword}"
table_name = "activities"

# Call the function to upsert the data into the SQL Server table
upsert_dataframe_to_sql(activities_df, connection_string, table_name)