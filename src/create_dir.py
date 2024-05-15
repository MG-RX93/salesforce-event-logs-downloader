import os
import sys
import json
from dotenv import load_dotenv  # pip install python-dotenv

# Load environment variables from .env file
load_dotenv()

def validate_environment_variables():
    """
    Validates the necessary environment variables and returns them.
    Exits the program if any required environment variable is not set.
    """
    base_directory = os.getenv("EVENT_LOG_BASE_DIR")
    if base_directory is None:
        print("Error: EVENT_LOG_BASE_DIR environment variable is not set.")
        sys.exit(1)

    event_types_json = os.getenv("EVENT_TYPES_MAPPING")
    if event_types_json is None:
        print("Error: EVENT_TYPES_MAPPING environment variable is not set.")
        sys.exit(1)

    try:
        event_types_mapping = json.loads(event_types_json)
    except json.JSONDecodeError:
        print("Error: EVENT_TYPES_MAPPING environment variable is not a valid JSON string.")
        sys.exit(1)
    
    return base_directory, event_types_mapping

def create_directory_structure(base_dir, financial_year, quarter, sprint_name, event_types):
    """
    Creates a directory structure based on the provided parameters.
    """
    # Ensure that the base directory is expanded properly if it contains a tilde (~)
    base_dir = os.path.expanduser(base_dir)

    for original_event_type, directory_name in event_types.items():
        # Construct the full path for each event type directory
        full_dir_path = os.path.join(
            base_dir, financial_year, quarter, sprint_name, directory_name
        )

        # Create the directory structure, avoiding errors if the directory already exists
        os.makedirs(full_dir_path, exist_ok=True)

        # Print the path of the created directory for verification
        print(f"Directory created: {full_dir_path}")

def main():
    """
    Main function to handle command line arguments and initiate directory creation.
    """
    # Ensure the script is run with the correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python create_directories.py <FinancialYear> <Quarter> <SprintName>")
        sys.exit(1)

    # Parse command line arguments
    financial_year = sys.argv[1]
    quarter = sys.argv[2]
    sprint_name = sys.argv[3]

    # Validate and retrieve necessary environment variables
    base_directory, event_types_mapping = validate_environment_variables()

    # Create directories based on the provided parameters
    create_directory_structure(
        base_directory, financial_year, quarter, sprint_name, event_types_mapping
    )

if __name__ == "__main__":
    main()
