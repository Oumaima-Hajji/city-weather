import json
import jsonschema
from google.cloud import bigquery
from google.cloud import storage

import jsonschema

def fetch_json_from_gcs(bucket_name, file_name, json_schema):
    """Fetches the JSON file from the specified GCS bucket and validates it."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    try:
        # Download the JSON data as bytes
        json_bytes = blob.download_as_bytes()
        
        # Decode the bytes to UTF-8 string
        json_data = json_bytes.decode("utf-8")
        
        # Validate the JSON data
        jsonschema.validate(json.loads(json_data), json_schema)
        
        return json_data

    except jsonschema.exceptions.ValidationError as e:
        print(f"JSON data validation error: {e}")
        return None

    except Exception as e:
        print(f"Error fetching JSON data: {e}")
        return None


def create_bigquery_table(dataset_id, table_id, schema):
    """Creates a BigQuery table with the specified schema."""
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    return table

def infer_bigquery_schema(json_data):
    """Infers the BigQuery schema from the JSON data."""
    example_json = json_data[:1000]  # Use a sample of the JSON data for schema inference
    try:
        schema = bigquery.SchemaField.from_api_repr(json.loads(example_json))
        return schema
    except Exception as e:
        raise RuntimeError(f"Failed to infer schema from JSON data: {e}")

def ingest_json_to_bigquery(json_data, dataset_id, table_id):
    """Ingests the JSON data into a BigQuery table."""
    schema = infer_bigquery_schema(json_data)
    if schema is None:
        # Handle the error, e.g., return or exit the script
        print("Failed to infer schema from JSON data. Exiting...")
        exit()
    
    table = create_bigquery_table(dataset_id, table_id, schema)
    
    # Load data into the table
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job = client.load_table_from_json(json_data, table, job_config=job_config)
    job.result()  # Wait for the job to complete
    
    if job.errors:
        raise RuntimeError(f"BigQuery job failed with errors: {job.errors}")

# Set your GCS bucket and JSON file name
bucket_name = "weather_data_oumaima"
file_name = "weather_data.json"

# Set your BigQuery dataset and table IDs
dataset_id = "weather_data"
table_id = "weather"

# Define the JSON schema
json_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "latitude": {
      "type": "number"
    },
    "longitude": {
      "type": "number"
    },
    "generationtime_ms": {
      "type": "number"
    },
    "utc_offset_seconds": {
      "type": "number"
    },
    "timezone": {
      "type": "string"
    },
    "timezone_abbreviation": {
      "type": "string"
    },
    "elevation": {
      "type": "number"
    },
    "hourly_units": {
      "type": "object",
      "properties": {
        "time": {
          "type": "string"
        },
        "temperature_2m": {
          "type": "string"
        },
        "relativehumidity_2m": {
          "type": "string"
        },
        "precipitation": {
          "type": "string"
        },
        "rain": {
          "type": "string"
        },
        "snowfall": {
          "type": "string"
        },
        "snow_depth": {
          "type": "string"
        },
        "weathercode": {
          "type": "string"
        },
        "visibility": {
          "type": "string"
        },
        "windspeed_10m": {
          "type": "string"
        }
      },
      "required": [
        "time",
        "temperature_2m",
        "relativehumidity_2m",
        "precipitation",
        "rain",
        "snowfall",
        "snow_depth",
        "weathercode",
        "visibility",
        "windspeed_10m"
      ]
    },
    "hourly": {
      "type": "object",
      "properties": {
        "time": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "temperature_2m": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "relativehumidity_2m": {
          "type": "array",
          "items": {
            "type": "number"
          }
        }
      },
      "required": [
        "time",
        "temperature_2m",
        "relativehumidity_2m"
      ]
    }
  },
  "required": [
    "latitude",
    "longitude",
    "generationtime_ms",
    "utc_offset_seconds",
    "timezone",
    "timezone_abbreviation",
    "elevation",
    "hourly_units",
    "hourly"
  ]
}


# Call the fetch_json_from_gcs function with the JSON schema
json_data = fetch_json_from_gcs(bucket_name, file_name, json_schema)

print(json_data)

# Check if JSON data is valid
if json_data is None:
    # Handle the error, e.g., return or exit the script
    print("JSON data is not valid. Exiting...")
    exit()

# Ingest the JSON data into BigQuery
ingest_json_to_bigquery(json_data, dataset_id, table_id)
