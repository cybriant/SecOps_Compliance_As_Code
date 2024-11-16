import json
from fpdf import FPDF



#Used the Create PDF with Python tutorial at:  https://www.youtube.com/watch?v=q70xzDG6nls&list=PLjNQtX45f0dR9K2sMJ5ad9wVjqslNBIC0 by Chart Explorers
#Some code copied or modified for use

class PDF(FPDF):
    """
    Note this class is a modified version of the code from the Create PDF with Python tutorial
    """

    def addHeader(self, title):
        """
        Creates a header for the document as there isn't a default header argument for FPDF.  Must
        be used after the add_page() function.
        :param title: The name of the title in the header of the compliance framework
        :return: None
        """
        self.set_font('helvetica', 'B', 20)
        self.cell(1, 10, title, border=False, ln=1)
        self.ln(1)

    def addDescription(self, description, fontSize=14, fontName="Times"):
        self.set_font(fontName, "", size=fontSize)
        self.multi_cell(0, 5, description)
        self.ln(1)


def json_to_pdf(json_data, dates=None, directory=None):
    #Create
    pdf = PDF("P", "mm", "Letter")

    #Set title of the PDF
    title_information = f"NIST CSF 2.0-{json_data['Subcategory']}-{json_data['Implementation Examples']}"
    pdf.set_title(title_information)
    print(f"Starting to export {title_information}")

    try:
        pdf.add_font('Courier New', '', 'Courier New.ttf', uni=True)
    except Exception as e:
        print(f"Add the Courier New font ttf file to the executing directory.  Full error:\n{e}")

    pdf.set_auto_page_break(auto=True)

    pdf.add_page()
    pdf.addHeader(title=title_information)
    #pdf.set_font("Times", '', size=14)

    pdf.addDescription(json_data['Function'])
    pdf.addDescription(json_data['Category'])
    pdf.addDescription(json_data['Category Description'], fontSize=12)
    pdf.addDescription(json_data['Subcategory'])
    pdf.addDescription(json_data['Subcategory Description'], fontSize=12)
    pdf.addDescription(json_data['Implementation Examples'])
    pdf.addDescription(json_data['Example Description'], fontSize=12)
    pdf.addDescription(f"Compliance Framework References:")
    pdf.addDescription(f"{json_data['Informative References']}", fontSize=12)
    pdf.addDescription(f"Vendor: {json_data['Vendor']}", fontSize=12)
    pdf.addDescription(f"Comments: {json_data['Comments']}", fontSize=12)

    pdf.add_page()
    pdf.addDescription('UDM Search Query:')
    pdf.addDescription(f"{json_data['Pretty Print Queries']}", fontSize=12, fontName="Courier New")

    #Here we check each set of JSON elements under each date, and we harvest their key names
    #This is done in case some dates have keys that don't appear in other dates for any odd reason
    allKeys = []
    for eachDate in dates:
        for eachGroup in json_data[eachDate]:
            for k, v in eachGroup.items():
                if k not in allKeys:
                    allKeys.append(k)

    #print(f"All my keys walk like this:\n{allKeys}")

    #We're now going to go through each date, add a page for the date
    #and add the date for the corresponding date.
    for eachDate in dates:
        # Add table data from JSON
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 5, eachDate, ln=1)
        pdf.ln(1)

        #Create copy of allKeys to build table for specific date
        dateList = [allKeys[:]]

        #Create list of lists to build table
        for eachGroup in json_data[eachDate]:
            groupValues = []
            #Cycle through each key/value which corresponds in order with the allKeys list created
            for eachKey in allKeys:
                for k, v in eachGroup.items():
                    #Check each dictionary key against eachKey from allKeys to determine if it's in the same position
                    #If in the same position, then append it to list representing a row in the table
                    if k == eachKey:
                        groupValues.append(v)
            #Append the set of groupValues to the dateList
            dateList.append(groupValues)

        #print(dateList)
        #The following code is modified from the FPDF2 documentation on how to create a simple example table
        #Set table font and style
        pdf.set_font("Times", "", 12)
        with pdf.table() as table:
            for data_row in dateList:
                row = table.row()
                for data_item in data_row:
                    row.cell(data_item)


    # Output usable PDF file
    pdf.output("/".join((directory, ".".join((title_information, "pdf")))), "F")



if __name__ == '__main__':
    from consts import DATES_TO_CHECK
    with open("sample_report_data.json", "r") as f:
        sample_json_data = json.load(f)

    sample_json_data = sample_json_data[0]

    json_to_pdf(sample_json_data, DATES_TO_CHECK, 'ComplianceReports')
