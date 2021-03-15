import requests
import base64
import io
from bs4 import BeautifulSoup as Soup
import pandas as pd 
import os
import openpyxl
import threading
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
i=0
report_id_list = []
#-----------------Getting URL Details------------------------------------------
username = input("Enter Qualys Username: ")
password = input("Enter the password: ")
excel_path = input(r"Enter the path where URL sheet with URL ID is present: ")
filename = input("Enter the filename(with extension): ")

full_path = excel_path + f"\{filename}"

wb_obj = openpyxl.load_workbook(full_path)
sheet_obj = wb_obj.active
data = sheet_obj.values
columns = next(data)[0:]
df = pd.DataFrame(data, columns= columns)

os.mkdir('./Reports')


#----------------Defining Delete Function--------------------------------------
def delete_was_report(report_id_list, payload, headers):
    
    for x in report_id_list:
        URL = 'https://qualysapi.qg2.apps.qualys.eu/qps/rest/3.0/delete/was/report/%d' % int(x)
        r = requests.post(URL, data = payload, headers=headers, verify=False)
        r.close()
		
		
    
#---------------------Defining Create Report Function--------------------------
def create_was_report(payload, headers):
    
    URL = "https://qualysapi.qg2.apps.qualys.eu/qps/rest/3.0/create/was/report"
    r = requests.post(URL, data = payload, headers=headers, verify=False)
    
    resp = r.text
    soup = Soup(resp,'lxml')
    report_id = soup.id.get_text()
    r.close()
    return(report_id)
	
	

#---------------------Defining Download Report Function--------------------------
def download_was_report(report_id, payload, headers):
    
    URL = 'https://qualysapi.qg2.apps.qualys.eu/qps/rest/3.0/download/was/report/%d' % int(report_id)
    
    print(f'Report for {was_name} is Downloading')
    
    r = requests.get(URL, headers=headers, verify=False)
    
    #---------Check if the report is generated or not--------------------------
    resp = r.text
    soup = Soup(resp,'xml')
    has_error_message = soup.find("errorMessage")
    if(str(has_error_message) != "None"):
        report_id = create_was_report(payload, headers)
        download_was_report(report_id, payload, headers)
        
    else:
    #-----------Report Generation successfull----------------------------------
        data = io.StringIO(r.text)
        
        #Write data in csv file
        with open(f'./Reports/Vuln Status Report({i}).csv', 'wb') as f:
            for line in data:
                f.write(line.encode('utf8'))
        
        print(f'Report for {was_name} downloaded')
        report_id_list.append(report_id)
        
        r.close()
        
        return("Done")
		


#---------------------Starting Report Download Process-------------------------
for index, row in df.iterrows():
    i+=1
    was_id = int(row['ID'])
    was_name = row['URL']
    
#---------------Setting Request header and Payload-----------------------------
    usrPass = str(username)+':'+str(password)
    data_bytes = usrPass.encode("ascii")
    b64Val = base64.b64encode(data_bytes)
    base64_message = b64Val.decode('ascii')
    
    headers = {
             'X-Requested-With': 'QualysPostman',
             'Content-Type': 'text/xml',
             'Authorization': f'Basic {base64_message}' 
         }
    
    payload = f'<ServiceRequest><data><Report><name><![CDATA[API Web Application Report]]></name><type>WAS_WEBAPP_REPORT</type><format>CSV</format><template><id>134040</id></template><config><webAppReport><target><webapps><WebApp><id>{was_id}</id></WebApp></webapps></target></webAppReport></config></Report></data></ServiceRequest>'
    
    
    #----------------To Create the WAS Report ID---------------------------------------
    
    report_id = create_was_report(payload, headers)
    
    #----------------To Download the WAS Report ID---------------------------------------
    
    download_message = download_was_report(report_id, payload, headers)
    
    #----------------To Delete the WAS Report -------------------------------------------   
    if(i%20==0):
        thread = threading.Thread(target=delete_was_report, args=[report_id_list, payload, headers])
        thread.start()
        thread.join()
        
        report_id_list.clear()
        print("All generated reports have been deleted")
        continue
    
input("All the reports have been downloaded. Press any key to exit: ")
