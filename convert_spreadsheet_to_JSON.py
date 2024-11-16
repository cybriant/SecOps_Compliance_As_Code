import csv, json, pandas

inputFile = "NIST_to_SecOps.xlsx"
outputFile = "NIST_CSF_2.0-SecOps.json"

def map_to_json(in_file_name=inputFile, out_file_name=outputFile):
    """
    Converts a compliance spreadsheet into a JSON file which can then be used to
    perform operations against a SecOps instance.
    :param in_file_name: This is the spreadsheet to convert to JSON.
    :param out_file_name: This is output JSON file name.
    :return: This is the JSON file name and data.
    """
    xls = pandas.read_excel(in_file_name)
    json_data = xls.to_json(orient='records')

    with open(out_file_name, 'w') as out_file:
        out_file.write(json_data)

    return {'filename': out_file_name, 'jsonData': json_data}

if __name__ == '__main__':
    map_to_json()