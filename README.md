# Web-Application-Scan-Report-Download-Automated-Process-in-Qualys
This repository contains the python file which automate Web Application Scan Report Download Process.

The script contains three process for Downloading the files:

  1. Creating of WAS Report ID.
      Inorder to download the report first the Qualys API would need to have a WAS Report ID. Fo that first process is to feed the file which contains the necessary URLs for which       the report has to be downloaded along with their WAS ID. (I have uploaded the sample file for reference.)
      
  2. Report Download Process.
      In this Process the reports will be downloaded taking the report id as a reference. The downloaded report will be in CSV Format and will be saved in ./Reports folder.
  
  3. Report Deletion Process.
      Since in Qualys there is a 200MB memory limit to save the reports therefore for large quantity of Report to be downloaded this process will automatically delete the               downloaded report from Qualys servers.
      
The reason for creating this script is because I have went through various repos for Qualys API integration and have found none of them useful for sucessfully connecting to the API, and also this is a full fleged complete Download system for those needed.

Note:- Kindly change the API URL as per the Qualys server address for making API Calls. This can be found in page no - 13 from the following link https://www.qualys.com/docs/qualys-was-api-user-guide.pdf
