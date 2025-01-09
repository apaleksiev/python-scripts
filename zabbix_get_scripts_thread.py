from pyzabbix import ZabbixAPI
import json

ZABBIX_USERNAME = 'user'
ZABBIX_PASSWORRD = 'pass'

zapi = ZabbixAPI("http://yourzabbixendpoint/zabbix/api_jsonrpc.php")
zapi.login(ZABBIX_USERNAME, ZABBIX_PASSWORRD)
print("Connected to Zabbix API Version %s" % zapi.api_version())

groups = ['DC1']

def get_items_for_group(zapi, group_id, start, limit):
    items = zapi.item.get(
        groupids=group_id,
        output=["itemid", "name", "key_", "hostid", "delay"],
        start=start,  # Set the start index for pagination
        limit=limit   # Set the limit for the number of items per page
    )
    filtered_items = [item for item in items if "scripts_win" in item['key_']]
    return filtered_items

grouped_items = {}
start = 0  # Initialize the start index
limit = 20  # Specify the number of items per page

for group_id in groups:
    grouped_items[group_id] = []
    while True:
        items = get_items_for_group(zapi, group_id, start, limit)
        if not items:
            break  # No more items to retrieve
        grouped_items[group_id].extend(items)
        start += limit  # Increment the start index for the next page

host_ids = set(item['hostid'] for items in grouped_items.values() for item in items)
host_info = zapi.host.get(hostids=list(host_ids), output=["host"])
host_name_mapping = {host['hostid']: host['host'] for host in host_info}

items_and_hosts = []

for group_id, items in grouped_items.items():
    print(f"Zabbix Custom scripts for datacenter {group_id}:")
    for item in items:
        host_names = [host_name_mapping.get(item['hostid'], "Unknown")]
        items_and_hosts.append({
            "Item Name": item['name'],
            "Item Key": item['key_'],
            "Item Delay": item['delay'],
            "Host Names": host_names
        })

json_file_path = "DC1_scripts_windows.json"

with open(json_file_path, "w") as json_file:
    json.dump(items_and_hosts, json_file, indent=2)

zapi.user.logout()
