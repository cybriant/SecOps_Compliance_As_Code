import csv

from google.oauth2 import service_account
from googleapiclient import _auth
#from google.auth.transport.requests import Request
from google.auth.transport import requests
#import requests
import json
import consts
import base64
from datetime import datetime
from urllib.parse import urljoin
import os
from time import sleep
import export_to_pdf
import warnings

class GoogleWebException(Exception):
    "Raised when Google API returns errors"
    #Used from Stack Exchange example:  https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
    # def __init__(self, message, errors):
    #     super().__init__(message)
    #
    #     self.errors = errors

    def __init__(self, message):
        self.message = message
def load_creds_into_google_credentials(inputFile, outputFile, credsType='BACKSTORY_API'):
    """
    Loads credentials from input file that has all types of credentials
    and outputs them to a file that only has the specified type creds file that is specified by credsType.
    :param inputFile: File that has multiple SecOps credential types.
    :param outputFile: File that has the specified type creds file that is specified by credsType.
    :param credsType: Specifies the credentials type to load.
    :return: http client object that has the specified type creds file that is specified by credsType.
    """

    #Load the original credentials file that has all of the different API key types
    with open(inputFile, 'r') as credsFile:
        creds = json.load(credsFile)

    #Load the specific base64 encoded string that has what will be dumped into a credentials file to be read
    myCreds = ""
    for each in creds['credentials']:
        if each['credentialType'] == credsType:
            myCreds = each['credential']
            #print(myCreds)

    #Decode the base64 credentials into plaintext
    credsDecoded = json.loads(base64.b64decode(myCreds).decode('utf-8'))
    print(credsDecoded)

    #Create the output file that has the decoded credentials in it
    with open(outputFile, 'w') as credsDumped:
        json.dump(credsDecoded, credsDumped)

    #Load the Google credentials into the Google auth framework
    return service_account.Credentials.from_service_account_file(outputFile, scopes=consts.SCOPES)

def get_events_by_udm_query(mySession, query, start_time, end_time, limit=100):
    """
    Get events by udm query
    This is a modified version of the GoogleChronicle SOAR Python function.
    Args:
        query (str): query to run
        start_time (str): start time
        end_time (str): end time
        limit (int): limit for results; Default limit is 100 items
    Returns:
        ([UdmQueryEvent]) list of UdmQueryEvent objects
    """
    #url = self._get_full_url("udm_search")
    url = _get_full_url("udm_search")

    params = {
        "time_range.start_time": start_time,
        "time_range.end_time": end_time,
        "query": query,
        "limit": limit
    }

    #request = Request()
    #response = mySession.get(url, params=params)
    response = mySession.request("GET", url, params=params)

    #Validation is disabled as this is not using the Google SOAR API directly
    #self.validate_response(response)

    #Not sure that the parser.build_udm_query_event_objects is necessary here as we're not putting it in Google
    #SOAR format
    #return self.parser.build_udm_query_event_objects(response.json())

    #Andrew modification:  Returning only the json response
    return response.json()


def _get_full_url(url_id, **kwargs):
    """
    Get full url from url identifier.
    This is a modified version of the GoogleChronicle SOAR Python function.

    Args:
        url_id (str): The id of url
        kwargs (str): Variables passed for string formatting
    Returns:
        (str): The full url
    """
    #return urljoin(self.api_root, consts.ENDPOINTS[url_id].format(**kwargs))
    return urljoin(consts.API_URL, consts.ENDPOINTS[url_id].format(**kwargs))

def convert_date(start_date, end_date=None):
    """
    Takes a single date or date range, and coverts it to a string that can be used by Chronicle.
    :param start_date:  Start date of search range.  Must be in the form MM-DD-YYYY.
    :param end_date: End date of search range.  Must be in the form MM-DD-YYYY.  If not specified, the end
    date is assumed to be the same day as the start date, but at the end of the 24 hour period.
    :return:  Two strings in the format "%Y-%m-%dT%H:%M:%SZ%z
    """
    if end_date == None:
        end_date = start_date

    start_date_components = start_date.split("-")
    end_date_components = end_date.split("-")

    #Checking to verify that the date is a valid date
    try:
        datetime.strptime(start_date, "%m-%d-%Y")
        datetime.strptime(end_date, "%m-%d-%Y")
    except ValueError:
        print("Not a valid date")

    #Checking to verify that the end date is after the start date
    try:
        datetime.strptime(start_date, "%m-%d-%Y") <= datetime.strptime(end_date, "%m-%d-%Y")
    except ValueError:
        print(f"The end date ({end_date}) is before the start date ({start_date}).")

    #Change to the format that Google Chronicle API can ingest
    new_start_date = '-'.join((start_date_components[2], start_date_components[0], start_date_components[1])) + "T00:00:01.000Z"
    end_date_components = '-'.join((end_date_components[2], end_date_components[0], end_date_components[1])) + "T23:59:59.000Z"

    #Return a dictionary with the startTime and endTime which is usable by the Google API
    return {"startTime": new_start_date, "endTime": end_date_components}


def load_compliance_json(compliance_json_file):
    """
    Loads compliance json file into a dictionary.  Note:  This will load any query that has a Difficulty of
    "Done" or "Unverified" and API is "UDM Search with YL2"
    :param compliance_json_file: Loads a JSON compliance file already converted having used the
    convert_spreadsheet_to_JSON.py script.
    :return: A dictionary with the relevant compliance data.
    """
    #We create a list of dictionaries with only the compliance elements that are applicable to UDM Searches
    cleanedList = []

    with open(compliance_json_file, 'r') as complianceFile:
        jsonData = json.load(complianceFile)

        for each in jsonData:
            #We specify for UDM searchable data.  We only include "Done" or "Unverified"
            #searches as "In Progress" searches can return errors
            if each['API'] == "UDM Search with YL2" and each['Difficulty'] in ("Done", "Unverified"):
                cleanedList.append(each)

    return cleanedList



# Test authentication is successful - This is modified from the Google example_usage.py
def test_authentication(auth_credentials):
    try:
        # Fetch the token w object request
        #request = Request()


        # Try to refresh creds w new token if the current one is expired
        #auth_credentials.refresh(request)

        # If there is no exception we have successfully authenticated with new token.
        print("Access Token obtained, auth successful.")
    except Exception as s:
        # If there was an error authenticating, let user know
        print(f"Authentication Failed: {s}")


if __name__ == '__main__':
    useDummyData = consts.USE_DUMMY_DATA
    #Set how long to sleep when creating UDM reports; if useDummyData is True then there is no wait during
    #UDM queries, otherwise, there is a 2 second wait between queries to avoid exhaustin the API
    sleepTimer = 2
    if useDummyData == True:
        sleepTimer = 0
        #If using dummyData don't output warnings
        warnings.filterwarnings("ignore")
        with open(consts.DUMMY_DATA_1, 'r') as dummyFile:
            dummyJson = json.load(dummyFile)
            dummyJson = dummyJson['Sheet1']


    complianceReportDirectory = "ComplianceReports"

    #Create a directory to store the reports
    if not os.path.exists(complianceReportDirectory):
        os.mkdir(complianceReportDirectory)

    #Load credentials
    someCreds = load_creds_into_google_credentials(consts.ALL_CREDS_FILE, consts.OUTPUT_CREDS_FILE, credsType='BACKSTORY_API')


    udm_http_client = requests.AuthorizedSession(someCreds)

    #Build the http_client to connect To Chronicle - old version recommended from Google documentation that's wrong
    #http_client = _auth.authorized_http(someCreds)

    ##### The following can be used to run individual UDM queries
    #Convert the dates given by user to UDM search compatible dates
    searchDates = convert_date(consts.test_start_date, consts.test_end_date)

    # #Run the UDM query to gather data
    # udm_data = get_events_by_udm_query(udm_http_client, consts.test_query_aggregate, searchDates['startTime'], searchDates['endTime'], limit=consts.LIMIT)
    # print(udm_data)
    # #####

    def run_main():
        #Load compliance list
        compliance_list = load_compliance_json(consts.COMPLIANCE_JSON_FILE)
        #Change to compliance directory
        #os.chdir(complianceReportDirectory)

        #Iterate through each compliance item
        for i, eachItem in enumerate(compliance_list):
            #Iterate through each date
            for eachDate in consts.DATES_TO_CHECK:
                #We briefly sleep before each query to avoid making the Google API gods angry
                sleep(sleepTimer)
                #Convert our dates or our UDM searches
                searchDate = convert_date(eachDate)

                if useDummyData == True:
                    compliance_list[i][eachDate] = dummyJson
                else:
                    try:
                        #Execute the corresponding UDM query
                        print(f"Running compliance report for subcategory: {eachItem['Subcategory']} {eachItem['Implementation Examples']}: {eachDate}")
                        return_udm_data = get_events_by_udm_query(udm_http_client, eachItem["Pretty Print Queries"],
                                                           searchDate['startTime'], searchDate['endTime'], limit=consts.LIMIT)

                        if 'error' in return_udm_data:
                            raise GoogleWebException(return_udm_data)

                        #Append the UDM data to each corresponding date for the compliance item
                        compliance_list[i][eachDate] = return_udm_data

                    except GoogleWebException as gwe:
                        print(f"Google API issue: {gwe}")
                        with open("somethingBroke.log", 'a') as somethingBrokeFile:
                            theText = f"\nSubcategory: {eachItem['Subcategory']}  Example: {eachItem['Implementation Examples']}:  {gwe}"
                            somethingBrokeFile.writelines(theText)
                        pass

                    except Exception as e:
                        print(f"Something broke, here is the error\n{e}")
                        with open("somethingBroke.log", 'a') as somethingBrokeFile:
                            theText = f"\nSubcategory: {eachItem['Subcategory']}  Example: {eachItem['Implementation Examples']}:  {e}"
                            somethingBrokeFile.writelines(theText)

        #Create JSON version of report data
        with open('/'.join((complianceReportDirectory, 'outputJsonFile.json')) , 'w') as outputFile:
            json.dump(compliance_list, outputFile)

        #Create PDF reports of each compliance example
        for each in compliance_list:
            #Export each compliance example to PDF using the appropiate dates and directory
            export_to_pdf.json_to_pdf(each, consts.DATES_TO_CHECK, '.'.join((complianceReportDirectory, "/")))

    run_main()