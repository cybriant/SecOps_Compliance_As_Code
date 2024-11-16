API_URL = 'https://backstory.googleapis.com'
SCOPES = ["https://www.googleapis.com/auth/chronicle-backstory"]
#ALL_CREDS_FILE = 'demo_cybriant_all_creds.json'
ALL_CREDS_FILE = r'C:\Users\AndrewHamilton\OneDrive - Primus Services, LLC dba Cybriant\temp\SecOps\demo_cybriant_all_creds.json'
#OUTPUT_CREDS_FILE = 'demo_cybriant_scoped_creds.json'
OUTPUT_CREDS_FILE = r'C:\Users\AndrewHamilton\OneDrive - Primus Services, LLC dba Cybriant\temp\SecOps\demo_cybriant_scoped_creds.json'
MAX_RETRIES = 40
LIMIT = 50
DEFAULT_LIMIT = 100
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DUMMY_DATA_1 = "JSON_dummy_data_host-destIP-count.json"
COMPLIANCE_FIELD_NAMES = ['Category', 'Category Description', 'Subcategory', 'Subcategory Description', 'Implementation Examples',
                          'Example Description', 'Informative References', 'Exportable From SIEM', 'API',
                          'Difficulty', 'Comments', 'Linked Query', 'Vendor', 'Query Version', 'Dashboard Name',
                          'Pretty Print Queries'
                          ]
COMPLIANCE_JSON_FILE = 'NIST_CSF_2.0-SecOps.json'
DATES_TO_CHECK = ["10-20-2024", "09-20-2024", "08-20-2024"]
USE_DUMMY_DATA = False

ENDPOINTS = {
    "udm_search": "v1/events:udmSearch",
    'get_reference_list': 'v2/lists/{reference_list_name}?view={view}'
}


#This is a test query taken from the spreadsheet.  If the formatting works here, it should be able to take the queries
#from the spreadsheet and utilize them correctly.
test_query_aggregate = """
$hostname = group($e.principal.hostname,$e.target.hostname,$e.src.hostname,$e.intermediary.hostname,$e.observer.hostname,$e.principal.asset.hostname,$e.src.asset.hostname,$e.target.asset.hostname)
$hostname = /.*/
match:
    $hostname
outcome:
	$logsSeen = array_distinct($e.metadata.log_type)
order:
	$hostname
"""

#Simple query to verify that things
test_query_simple = 'metadata.event_type="GENERIC_EVENT"'

#Date ranges for testing
test_start_date = "10-16-2024"
test_end_date = "10-20-2024"

