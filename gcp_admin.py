from google.cloud import storage
from google.oauth2 import service_account
import json
from utils import *



def upload_json_to_bucket(bucket_name, file_name, json_data, key_file_path):
    credentials = service_account.Credentials.from_service_account_file(key_file_path)
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    blob.upload_from_string(json.dumps(json_data), content_type='application/json')
    print(f'Successfully uploaded {file_name} to {bucket_name}')




bucket_name = 'weather_data_oumaima'
file_name = 'weather_data.json'
json_data = daily_payload() # Call your get_weather_api() function to get the JSON payload
key_file_path = '/Users/oumaima/Desktop/weather_project/city-weather/credentials.json'  # Replace with the actual path to your service account private key file

upload_json_to_bucket(bucket_name, file_name, json_data, key_file_path)
