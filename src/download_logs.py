import sys
import subprocess
import os
import json
from dotenv import load_dotenv
from query import main as get_salesforce_data

load_dotenv()

domain_name = os.getenv("SF_DOMAIN_NAME")
api_version = os.getenv("SF_VERSION_NUMBER")
output_directory = os.getenv("OUTPUT_DIRECTORY")
current_sprint_directory = os.getenv("CURRENT_SPRINT_DIRECTORY")
event_types_mapping = json.loads(os.getenv("EVENT_TYPES_MAPPING"))
event_query_pairs = json.loads(os.getenv("EVENT_QUERY_PAIRS"))

def format_date(log_date):
    return log_date.split("T")[0]

def get_valid_event_type(event_type):
    return event_type.replace("/", "_")

def get_converted_event_type(valid_event_type):
    if valid_event_type in event_types_mapping:
        return event_types_mapping[valid_event_type]
    else:
        print(f"Warning: Unmapped event type '{valid_event_type}'. Using default conversion.")
        return valid_event_type.upper()

def create_output_directory(log_date, event_type):
    formatted_date = format_date(log_date)
    valid_event_type = get_valid_event_type(event_type)
    converted_event_type = get_converted_event_type(valid_event_type)

    dynamic_output_directory = os.path.join(current_sprint_directory, converted_event_type)
    os.makedirs(os.path.expanduser(dynamic_output_directory), exist_ok=True)
    
    return formatted_date, valid_event_type, dynamic_output_directory

def construct_output_file_name(formatted_date, valid_event_type):
    return f"{formatted_date}_{valid_event_type}.csv"

def construct_download_url(domain_name, api_version, record_id):
    return f"https://{domain_name}/services/data/v{api_version}/sobjects/EventLogFile/{record_id}/LogFile"

def construct_output_file_path(dynamic_output_directory, output_file_name):
    return os.path.expanduser(f"{dynamic_output_directory}/{output_file_name}")

def construct_curl_command(download_url, access_token, output_file):
    curl_command = [
        "curl",
        download_url,
        "-H",
        f"Authorization: Bearer {access_token}",
        "-H",
        "X-PrettyPrint:1",
        "-o",
        output_file,
    ]
    return curl_command

def print_curl_command(curl_command):
    curl_command_str = (
        " ".join(curl_command[:2])
        + " "
        + " ".join([f'"{arg}"' if " " in arg else arg for arg in curl_command[2:]])
    )
    print(curl_command_str)

def execute_curl_command(curl_command, record_id, output_file):
    try:
        subprocess.run(
            curl_command,
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        print(f"Downloaded {record_id} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {record_id}: {e}")

def download_event_log_files(event_type, query_file):
    response, access_token = get_salesforce_data(query_file)

     # Extract record IDs from the query result
    data = [
        (record["Id"], record["LogDate"], record["EventType"])
        for record in response["records"]
    ]

    for record_id, log_date, event_type in data:
        formatted_date, valid_event_type, dynamic_output_directory = create_output_directory(log_date, event_type)

        output_file_name = construct_output_file_name(formatted_date, valid_event_type)
        download_url = construct_download_url(domain_name, api_version, record_id)
        output_file = construct_output_file_path(dynamic_output_directory, output_file_name)

        curl_command = construct_curl_command(download_url, access_token, output_file)
        print_curl_command(curl_command)

        execute_curl_command(curl_command, record_id, output_file)

if __name__ == "__main__":
    for event_type, query_file in event_query_pairs.items():
        print(f"Processing event type: {event_type}, query file: {query_file}")
        download_event_log_files(event_type, query_file)
