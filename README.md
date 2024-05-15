# salesforce-event-logs-downloader
Python scripts for automated downloading of Salesforce Event Log Files (ELF) using customizable filters. Streamline log retrieval for audits, compliance, or monitoring with minimal setup.

## Project setup


## .env file setup
- Use the below sample & set the values accordingly.
```env
# .env

# salesforce auth params
SF_CONSUMER_KEY=placeholder
SF_CONSUMER_SECRET=placeholder
SF_USERNAME=placeholder
SF_PASSWORD=placeholder
SF_AUTH_URL=https://yourdomain.sandbox.my.salesforce.com/services/oauth2/token
SF_TOKEN_LIFETIME=3600
SF_VERSION_NUMBER=59.0

# salesforce query params
SF_DOMAIN_NAME=yourdomain.sandbox.my.salesforce.com

# directory params
OUTPUT_DIRECTORY=placeholder
CURRENT_SPRINT_DIRECTORY=placeholder
EVENT_LOG_BASE_DIR=placeholder
```

## Create directories locally to store downloaded files
- To keep things uniform and organized, the directory setup uses parameters like Financial Year, Quarter & Sprint name.
- Pass the Financial Year, Quarter & Sprint name as parameters
```bash
python3 ./scripts/python/cURL/create_dir.py FY2024 Q3 SPRINT_T                                                                                                                                                                                                                                            
```

## Download Event Logs
- Run the below command to download event logs.
```bash
python3 ./scripts/python/cURL/download_elf.py ./scripts/python/cURL/soql/event_logs.soql
```