import requests
from urllib.parse import urlencode

# Define your client ID and client secret
client_id = "112924"
client_secret = "2c798d346ee633d30aad9c681a9d0927c52230d1"

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
else:
    print(f'Error: Unable to retrieve access token. Status code: {response.status_code}')
    print(response.json())