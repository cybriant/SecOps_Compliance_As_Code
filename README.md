# SecOps_Compliance_As_Code
 
This project is by Andrew Hamilton for Georgia Tech Practicum CS 6727 OCY Fall 2024

## Directions
***NOTE***:  This project assumes that you already have your SecOps credential file.  Please note, that these steps use the original version of the credentials file, and not the extracted elements from the individual API from the base64 encoding.  These steps will extract the base64 credentials for you. 

After clonining the repo (or simply downloading the script needed perform the following):

1. Execute "convert_spreadsheet_to_JSON.py" to create the JSON mapping from the latest version of the compliance framework Excel spreadsheet. _Note:  You must have the appropriate compliance in the same directory, and if it is different from the default (NIST_to_SecOps.xlsx) you edit and update the convert_spreadsheet_to_JSON.py file to the appropriate "in_file_name"_
2. Edit the consts.py to have the applicable variables for your environment.  Variables are explained under the Files section of this README.
3. Execute udm_search.py.  For example, on Windows:  "python3.exe udm_search.py" and on Linux:  "python3 udm_search.py"
4. By default, the udm_search.py script will create the "ComplianceReports" folder, and then populate all of the respective PDF reports in that folder.  Additionally, it will drop the JSON data in that folder.

**Please note**:  SecOps does not yet support Aggregate Queries from the API.  It is expected that this feature that can currently be run in the UDM Search Console in the Web UI for SecOps will be available in the near future for the API.  The Pretty Print Queries in the Excel spreadsheet can be run in the Web UI to gather the corresponding compliance evidence data from the SIEM.


## Files
### NIST_to_SecOps.xlsx  
This is an Excel file from which a JSON file will be created and used by the compliance scripts.  The file specifies all of the attributes that can be used in the compliance reports as well as the UDM queries that will executed in Google SecOps.  The file in the repository is applicable to NIST CSF 2.0, but can be used as a template for other compliance frameworks.  The following is a summary of the columns present:

**Function**:  Highest level of function for the framework (NIST:  Identify, Protect, Detect, Respond, and Recover) 

**Category**:  Individual categories within the hierarchical Function.

**Category** Description:  Description of the Category.

**Subcategory**:  Further refinement of a topic within a Category.

**Subcategory Description**:  Description of the subcategory.

**Implementation Examples**:  Individual examples of potential sources for evidence to determine compliance within a framework.

**Example Description**:  A high level description of the Implementation Example.

**Informative References**:  Compliance framework references that can be used as a crosswalk.  *Note:  The example at hand is not a one-to-one comparison to the compliance 
reference.  Instead, this specific example may serve to fulfill some or all of the referenced framework.*

**Exportable From SIEM**:  Whether evidence can be obtained from a SIEM to fulfill this Implementation Example.

**API**:  Whether the SIEM API may be used, or whether a corresponding API may have future functionality to be used with the Implementation Example.

**Difficulty**:  Current state in implementing the Implementation Example:  Custom, Done, In Progress, Unverified

**Comments**:  Expert opinion on how the evidence may be obtained from a SIEM, comments on current status of the implementation, or general comments about the Implementation Example.

**Linked Query**:  Specifies if the Implementation Example can be fulfilled with an and already written query, and provides a reference to that query.

**Vendor**:  If a query is vendor specific, this specifies to which vendors the Pretty Print Query will apply.

**Query Version**:  Specifies the current query version.  Alpha and Beta queries may or may not work.

**Dashboard Name**:  If an YARA-L Aggregate Query cannot be used to satify the Implementation Example, this specifies the SecOps Dashboard Name that will satisfy the requirement.

**Pretty Print Queries**:  A pretty print version of the YARA-L Aggregate Query that will be executed in SecOps.

**API Queries**:  Deprecated.  Unused.
***

### convert_spreadsheet_to_JSON.py
This script takes a flat compliance spreadsheet and converts it to a JSON file.  _Note:  The file must be flat and have no need of nested processing._

***Functions***  
**map_to_json(in_file_name=inputFile, out_file_name=outputFile):**  
Converts a compliance spreadsheet into a JSON file which can then be used to
perform operations against a SecOps instance.
:param in_file_name: This is the spreadsheet to convert to JSON.
:param out_file_name: This is output JSON file name.
:return: This is the JSON file name and data.
 ***

### consts.py
This contains the most important variables for execution of the script.  It provides a common place to store variables that may be used across multiple scripts, and also acts as holding place for variables for testing future fuctionality.

***Functions***  
**API_URL**:  The Google Backstory URL for API usage.

**SCOPES**:  Google APIs that may be used by the scripts.

**ALL_CREDS_FILE**:  This file contains the consolidated credentials that Google Support provides.  This credential file will have the API credential for every SecOps API in JSON format.  The individual API credentials must be extracted from the appropriate JSON key for the corresponding API.

**OUTPUT_CREDS_FILE**:  This the file that contains the extracted credentials for a specific API from the ALL_CREDS_FILE.

**MAX_RETRIES**:  (Currently unused) In the case of an error, how many times should the script attempt to retry the query.

**LIMIT**:  Specify what the standard limit for results should be.  This is especially important with non-aggregate queries as each JSON result returns a SIGNIFICANT amount of JSON data from the Backstory API.

**DEFAULT_LIMIT**:  If the LIMIT constant isn't specified, then the DEFAULT_LIMIT will be used in its place.

**TIME_FORMAT**:  Date/time format that is usable by the Backstory API.

**DUMMY_DATA_1**:  File with a set of JSON formatted dummy data for testing out reporting.

**COMPLIANCE_FIELD_NAMES**:  (Unused) The set of fields used in the compliance Excel spreadsheet.  Allows for building fields for the Python csv module for DictReader/DictWriter.

**COMPLIANCE_JSON_FILE**:  This is the name of the file generated from the *convert_spreadsheet_to_JSON.py* script.

**DATES_TO_CHECK**:  List of dates specified for gathering compliance date.  At least one date must be specified.

**USE_DUMMY_DATA**:  (True/False) Determines whether the *udm_search.py* script will use dummy data from DUMMY_DATA_1 for creating the report, or if it will instead attempt to harvest the datat from the Backstory API.

**ENDPOINTS**:  List of API endpoints to use with the Backstory API.

**test_query_aggregate**:  Simple YARA-L query to test aggregate query functionality against the Backstory API.

**test_query_simple**:  Simple UDM search query to test query search functionality against the Backstory API.

**test_start_date** and **test_end_date**:  Used for testing YARA-L/UDM Queries against date ranges instead of specific days as is done in DATES_TO_CHECK.
***


### udm_search.py
This is the primary executable script for gathering data from the Backstory API.  Run on its own (with DUMMY_DATA = False), it will run all compliance queries against the Backstory API for all dates specified in DATES_TO_CHECK.  Afterwards, it will create a compliance folder (by default:  ComplianceFolder/), and store the results from the queries in a JSON file in that directory called "outputJsonFile.json".  Afterwards, it will export compliance data to PDF using the *export_to_pdf.py* script.

***Functions***  
**class GoogleWebException(Exception)**  
This is a custom class created to be raised when Google API returns errors.  This enables error reporting instead of them being obscured.

**load_creds_into_google_credentials(inputFile, outputFile, credsType='BACKSTORY_API')**  
Loads credentials from input file that has all types of credentials
and outputs them to a file that only has the specified type creds file that is specified by credsType.  
:param inputFile: File that has multiple SecOps credential types.  
:param outputFile: File that has the specified type creds file that is specified by credsType.  
:param credsType: Specifies the credentials type to load.  
:return: http client object that has the specified type creds file that is specified by credsType.  

**get_events_by_udm_query(mySession, query, start_time, end_time, limit=consts.DEFAULT_LIMIT)**  
Get events by udm query  
This is a modified version of the GoogleChronicle SOAR Python function.  
Args:  
    query (str): query to run  
    start_time (str): start time  
    end_time (str): end time  
    limit (int): limit for results; Default limit is 100 items  
Returns:  
    ([UdmQueryEvent]) list of UdmQueryEvent objects  

**_get_full_url(url_id, **kwargs)**  
Get full url from url identifier.  
This is a modified version of the GoogleChronicle SOAR Python function.  

Args:  
    url_id (str): The id of url  
    kwargs (str): Variables passed for string formatting  
Returns:  
    (str): The full url  

**convert_date(start_date, end_date=None)**  
Takes a single date or date range, and coverts it to a string that can be used by Chronicle.  
:param start_date:  Start date of search range.  Must be in the form MM-DD-YYYY.  
:param end_date: End date of search range.  Must be in the form MM-DD-YYYY.  If not specified, the end
date is assumed to be the same day as the start date, but at the end of the 24 hour period.  
:return:  Two strings in the format "%Y-%m-%dT%H:%M:%SZ%z  

**load_compliance_json(compliance_json_file)**    
Loads compliance json file into a dictionary.  *Note:  This will load any query that has a Difficulty of
"Done" or "Unverified" and API is "UDM Search with YL2"*  
:param compliance_json_file: Loads a JSON compliance file already converted having used the
convert_spreadsheet_to_JSON.py script.  
:return: A dictionary with the relevant compliance data.  

**test_authentication(auth_credentials)**
This is an authentication test script that has modified from the Google Example authenication script.  It enables a person to verify that their credentials work with the Backstory API.  *Note:  As is, it is unusable due to modifications and testing.  You will need to take it as an example an modify to your own needs.*

**run_main()**:  
This is a function defined under the *if __name__ == '__main__':* block of the script and the function *run_main() is also the last line of the script.  This function executes the all of the necessary functions to acquire compliance data from the Google Backstory API.  It will then use the *export_to_pdf.py* script to generate the compliance PDF files.  Commenting out the very last line of this script (which is the *run_main() function) allows for testing specific funcions within the script (without the need to run everything).
***

### Courier New.ttf  
True type font necessary for the *export_to_pdf.py* script to run.
***

### somethingBroke.txt  
When things break in the *udm_search.py* file, the error messages are written to this file.  This allow for capturing Google error messages, and Google API error codes.
