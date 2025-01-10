#script to automate site24/7 monitoring for microservices in new DCs. Change tokens and IDs as required.
import requests
import json
import pprint

ACCESS_URL = "https://accounts.zoho.com/oauth/v2/token"
MONITORS_URL = "https://www.site24x7.com/api/monitors"
new_dc = "delta"
monitors = [microservice1", "microservice2", "microservice3"]

access_data = {
    "client_id": "<your_client_id>", 
    "client_secret": "<your_secret>", 
    "refresh_token": "<your_refresh_token>", 
    "grant_type": "refresh_token"
    }

access_request = requests.post(ACCESS_URL, data=access_data)
access_auth = access_request.json()
access_token = access_auth['access_token']
headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json;version=2.1",
    "Authorization": f"Zoho-oauthtoken {access_token}"
}

for i in monitors:
    if i == "Microservice1":
        data = {
            "display_name": f"{new_dc} Microservice1",
            "type": "URL",
            "website": f"https://{new_dc}.your-endpoint.com/v1/cxf",
            "check_frequency": 5,
            "timeout": 15,
            "http_method": "G",
            "location_profile_id": "201960000000025021",
            "notification_profile_id": "201960000000025063",
            "threshold_profile_id": "201960000000039009",
            "user_group_ids":[
                "201960000000025003",
                "201960000012995043"
            ],
            "use_ipv6": False,
            "request_content_type": "F",
            "monitor_groups": [
                "201960000000091087"
            ],
            "third_party_services": [
                "201960000001961001"
            ]
        }   
        r = requests.post(MONITORS_URL, json=data, headers=headers)
        print(r.status_code)

    if i == "Microservice2":
        data = {
            "display_name": f"{new_dc} Microservice2",
            "type": "URL",
            "website": f"https://opscheck-api-{new_dc}.your-endpoint.com/v1/microservice2",
            "check_frequency": 5,
            "timeout": 15,
            "http_method": "G",
            "location_profile_id": "201960000000025021",
            "notification_profile_id": "201960000000025063",
            "threshold_profile_id": "201960000000039009",
            "user_group_ids":[
                "201960000000025003",
                "201960000012995043"
            ],
            "use_ipv6": False,
            "request_content_type": "F",
            "monitor_groups": [
                "201960000003808005"
            ],
            "third_party_services": [
                "201960000001961001"
            ]
        }
        r = requests.post(MONITORS_URL, json=data, headers=headers)
        print(r.status_code)

    if i == "Microservice2":
        data = {
            "display_name": f"{new_dc} Microservice3",
            "type": "URL",
            "website": f"https://microservice3-{new_dc}.your-endpoint.services/healthcheck",
            "check_frequency": 5,
            "timeout": 15,
            "http_method": "G",
            "location_profile_id": "201960000000025021",
            "notification_profile_id": "201960000000025063",
            "threshold_profile_id": "201960000000039009",
            "user_group_ids":[
                "201960000000025003",
                "201960000012995043"
            ],
            "use_ipv6": False,
            "request_content_type": "F",
            "monitor_groups": [
                "201960000003926015"
            ],
            "third_party_services": [
                "201960000001961001"
            ]
        }
        r = requests.post(MONITORS_URL, json=data, headers=headers)
#        pprint.pprint(json.loads(r.content))
        print(r.status_code) 
