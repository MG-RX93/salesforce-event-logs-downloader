import sys
import requests
import os
from dotenv import load_dotenv  # Make sure to install the package using `pip install python-dotenv`
from auth import get_access_token

# Load environment variables from .env file
load_dotenv()

def get_soql_query_from_file(file_path):
    """
    Reads the SOQL query from a given file.

    Parameters:
    - file_path: A string representing the path to the .soql file.

    Returns:
    - A string containing the SOQL query.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    """
    with open(file_path, "r") as file:
        return file.read().strip()

def execute_soql_query(query):
    """
    Executes a SOQL (Salesforce Object Query Language) query against the Salesforce API.

    Parameters:
    - query: A string representing the SOQL query to be executed.

    Returns:
    - A dictionary containing the JSON response from the Salesforce API.

    Raises:
    - requests.exceptions.RequestException: If the query execution fails or the response status code is not 200.
    """
    access_token, instance_url = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    version_number = os.getenv("SF_VERSION_NUMBER")  # Ensure SF_VERSION_NUMBER is defined in .env

    query_url = f"{instance_url}/services/data/v{version_number}/query/"

    response = requests.get(query_url, headers=headers, params={"q": query})
    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"Query failed: {response.text}")
    return response.json(), access_token

def main(query_input):
    """
    Main function that processes the input to determine if it is a file path or a direct query string,
    then executes the query & returns the results.

    Parameters:
    - query_input: A string that can either be a file path to a .soql file containing a SOQL query or a direct SOQL query string.

    Returns:
    - A dictionary containing the query results.
    """
    soql_query = query_input
    if os.path.isfile(query_input):
        soql_query = get_soql_query_from_file(query_input)

    return execute_soql_query(soql_query)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <PATH_TO_QUERY_FILE>.soql")
        sys.exit(1)

    query_file = sys.argv[1]

    try:
        query_result = main(query_file)
        print(query_result)  # Print the query result to the console
    except FileNotFoundError:
        print(f"The file {query_file} does not exist.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Query failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

