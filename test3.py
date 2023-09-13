import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

# Replace these values with your actual Strava application's credentials
client_id = os.environ.get('strava_client_id')
client_secret = os.environ.get('strava_client_secret')
username = os.environ.get('mssqlusername')
server = os.environ.get('mssqlservere')
database = os.environ.get('mssqldatabase')
password = os.environ.get('mssqlpassword')

# Create a connection string
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Establish a connection to the SQL Server
    conn = pyodbc.connect(connection_string)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a sample SQL query
    cursor.execute('SELECT @@version')
    
    # Fetch and print the result
    row = cursor.fetchone()
    if row:
        print("SQL Server Version:", row[0])

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the database connection
    conn.close()