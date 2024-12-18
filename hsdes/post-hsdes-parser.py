import requests
from requests_kerberos import HTTPKerberosAuth
import urllib3
import csv
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


counter = 0

def create_payload(send_email=False):
    payload = dict()
    payload["tenant"] = "client_platf"
    payload["subject"] = 'test_case_definition'

    field_list = [
        # {
        #     "client_platf.test_case_definition.automation_type": record.get(
        #         "automation_type", ""
        #     )
        # },
        {
            "client_platf.test_case_definition.automtion_status": 'not_planned'
        },
        {
            # "client_platf.test_case_definition.automation_developer": "tejast"

        },
        # {
        #     "client_platf.test_case_definition.automation_comments": "Can be planned"
        # },
        # {"client_platf.test_case_definition.jira_id": record.get("jira_id", "")},
        # {
        #     "client_platf.test_case_definition.deployment_status": record.get(
        #         "deployment_status", ""
        #     )
        # },
        {"send_mail": send_email},
    ]

    payload["fieldValues"] = field_list
    return payload


def update_hsd(hsd_id, payload):
    headers = {"Content-type": "application/json"}
    url = f"https://hsdes-api.intel.com/rest/article/{hsd_id}"
    payload_json = json.dumps(payload)

    response = requests.put(
        url, verify=False, auth=HTTPKerberosAuth(), headers=headers, data=payload_json
    )
    response.raise_for_status()
    global counter
    counter+=1
    print(f'{counter}) - {hsd_id}')
    if response.status_code == 200:
        print("Success!")
    else:
        print("error")


def push(hsd_id):
    payload = create_payload(
        send_email=False,
    )
    update_hsd(hsd_id=hsd_id, payload=payload)

if __name__ == "__main__":
    tcids = [
'16017375790',
'16017331279'

]

    fp = r"C:\Users\tejast\Downloads\iousbtbt_move_tonot_planned.txt"
    with open(fp, "r") as f:
        fl = f.readlines()
    a = [i.strip() for i in fl]
    print(a, len(a))
    # exit()

    for hsd_id in a:
       push(hsd_id)
       # break

