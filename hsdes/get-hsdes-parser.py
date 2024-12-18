import os
import json
from requests_kerberos import HTTPKerberosAuth
import requests
from pprint import pprint
import csv
import re

def get_hsd(hsd_id):
    headers = {"Content-type": "application/json"}
    url = f"https://hsdes-api.intel.com/rest/article/{hsd_id}"
    # payload_json = json.dumps(payload)

    response = requests.get(
        url, verify=False, auth=HTTPKerberosAuth(), headers=headers
    )
    if response.status_code != 200:
        return None
    resp = response.json()
    data=resp['data'][0]
    autmation_status = data['client_platf.test_case_definition.automtion_status']
    title = data['title']
    hsdStatus = data['status']
    status_reason = data['status_reason']
    deployment_status = data['client_platf.test_case_definition.deployment_status']
    cat = data['client_platf.test_case_definition.validation_category']

    print(f"{hsd_id} - {title} - {hsdStatus} - {status_reason} - {autmation_status} - {deployment_status}")
    # pprint(response.json())
    return hsd_id, title, cat, hsdStatus, status_reason, autmation_status, deployment_status

def write_line_to_csv(file_path, line_data):
    if not line_data:
        return
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(line_data)

def extract_hsd_id(file_name):
    match = re.search(r'\d+', file_name)
    if match:
        return match.group(0)
    return None

file_path = r'C:\Users\tejast\Downloads\manageabilityRailsReport.csv'
line_data = ['HSD ID','Title', 'Category', 'HSD Status', 'HSD Status Reason', 'Automation Status', 'Deployment Status']


cat3Path = r"C:\workspace\railsgit\2\frameworks.validation.platform-automation.rails2\src\rails\cases\manageability\cat2"
ids = set()
for i in os.listdir(cat3Path):
    id = extract_hsd_id(i)
    if id:
        ids.add(id)
print(ids)

# write_line_to_csv(file_path, line_data)
for i in ids:
    write_line_to_csv(file_path, get_hsd(i))