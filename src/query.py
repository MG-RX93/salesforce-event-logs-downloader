import sys
import requests
import os
from dotenv import load_dotenv
from auth import get_access_token

# Load environment variables
load_dotenv()

def get_soql_query_from_file(file_path):
    """Read SOQL query from a file."""
    with open(file_path, "r") as file:
        return file.read().strip()

def execute_soql_query(query):
    """Execute a SOQL query and return the JSON response."""
    access_token, instance_url = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    version_number = os.getenv("SF_VERSION_NUMBER")

    query_url = f"{instance_url}/services/data/v{version_number}/query/"
    response = requests.get(query_url, headers=headers, params={"q": query})

    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"Query failed: {response.text}")
    return response.json(), access_token

def main(query_input):
    """Process the input and execute the SOQL query."""
    # Determine if the input is a file path or a direct query
    if os.path.isfile(query_input):
        soql_query = get_soql_query_from_file(query_input)
    else:
        soql_query = query_input  # Treat the input as a direct query
    return execute_soql_query(soql_query)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <PATH_TO_QUERY_FILE>.soql or <DIRECT_SOQL_QUERY>")
        sys.exit(1)

    query_input = sys.argv[1]

    try:
        query_result = main(query_input)
        print(query_result)
    except FileNotFoundError:
        print(f"The file {query_input} does not exist.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Query failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
