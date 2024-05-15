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
EVENT_QUERY_PAIRS={"ApexExecution":"scripts/soql/event_logs/apex_execution.soql","ApexTrigger":"scripts/soql/event_logs/apex_trigger.soql","FlowExecution":"scripts/soql/event_logs/flows.soql","ApexUnexpectedException":"scripts/soql/event_logs/apex_exceptions.soql","LightningPageView":"scripts/soql/event_logs/ltg_page_view.soql"}

# directory params
OUTPUT_DIRECTORY=placeholder
CURRENT_SPRINT_DIRECTORY=placeholder
EVENT_LOG_BASE_DIR=placeholder
EVENT_TYPES_MAPPING={"ApexExecution":"APEX_EXECUTION","ApexTrigger":"APEX_TRIGGER","FlowExecution":"FLOW_EXECUTION","ApexUnexpectedException":"APEX_UNEXPECTED_EXCEPTION","LightningPageView":"LIGHTNING_PAGE_VIEW","API":"API"}

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
python3 ./scripts/python/cURL/download_logs.py
```