#Script was written in order to get scripts that were presented in Zabbix as "items"
#we had accumulated hundreds over the years and we needed to know how many were there, what their purpose was, and if they were even in use anymore and could be removed

from pyzabbix import ZabbixAPI
import json

ZABBIX_USERNAME = 'user'
ZABBIX_PASSWORRD = 'pass'

zapi = ZabbixAPI("http://yourzabbixendpoint/zabbix/api_jsonrpc.php")
zapi.login(ZABBIX_USERNAME, ZABBIX_PASSWORRD)
print("Connected to Zabbix API Version %s" % zapi.api_version())

""" DC1 = '101'
DC2 = '102'
DC3 = '103'
DC4 = '128'
DC5 = '164'
DC6 = '28'
"""

group_id = 101

# Define the list of strings to exclude from item keys
exclude_strings = ["scripts_linux", "scripts_win", "scripts_centralized", "scripts_solaris"]
hostnames = zapi.host.get(groupids=group_id, output=["name"])
items_and_hosts = []

for i in hostnames:
    host_id = i['hostid']
    items = zapi.item.get(output=["name", "key_", "delay"], hostids=host_id)
#    filtered_items = [item for item in items if all(exclude not in item["key_"] for exclude in exclude_strings)]
#    filtered_items = [item for item in items if not item["key_"].startswith("external") and all(exclude not in item["key_"] for exclude in exclude_strings)]

    filtered_items = [item for item in items if
                     not item["key_"].startswith("external") and
                     not item["name"].startswith("Prometheus Alert") and
                     all(exclude not in item["key_"] for exclude in exclude_strings)]

    if filtered_items:
        for item in filtered_items:
            items_and_hosts.append({
                "Hostname": i["name"],
                "Item Name": item["name"],
                "Item Key": item["key_"],
                "Item Delay": item["delay"]
            })

json_file_path = "DC_remaining_30_7.json"
with open(json_file_path, "w") as json_file:
    json.dump(items_and_hosts, json_file, indent=2)

zapi.user.logout()
