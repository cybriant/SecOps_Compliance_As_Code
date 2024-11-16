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
#### NIST_to_SecOps.xlsx  
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


#### convert_spreadsheet_to_JSON.py
This script takes a flat compliance spreadsheet and converts it to a JSON file.  _Note:  The file must be flat and have no need of nested processing._

***Functions***  
**map_to_json(in_file_name=inputFile, out_file_name=outputFile):**  
Converts a compliance spreadsheet into a JSON file which can then be used to
perform operations against a SecOps instance.
:param in_file_name: This is the spreadsheet to convert to JSON.
:param out_file_name: This is output JSON file name.
:return: This is the JSON file name and data.
 
