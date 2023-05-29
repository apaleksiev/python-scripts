from datetime import datetime, timedelta
import pytz
import boto3
from pyzabbix import ZabbixAPI
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ZABBIX_SERVER = 'https://zabbix.com/api'
ZABBIX_USERNAME = 'username'
ZABBIX_PASSWORD = 'password'
ZABBIX_GROUP_ID = '24'
USA1_REGION_NAME = 'us-east-1'
EUROPE1_REGION_NAME = 'eu-west-1'

def get_zabbix_hosts(zapi):
    hosts = zapi.host.get(groupids=ZABBIX_GROUP_ID, output=['name'])
    return [host['name'] for host in hosts]

def get_ec2_instances(region_name, tag_name):
    ec2 = boto3.resource('ec2', region_name=region_name)
    filters = [
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'tag:Name', 'Values': [tag_name]}
    ]
    return ec2.instances.filter(Filters=filters)

def check_maintenance_mode(zapi, region_name, hosts):
    for host in hosts:
        ec2_instances = get_ec2_instances(region_name, host)
        for instance in ec2_instances:
            uptime = datetime.now(pytz.utc) - instance.launch_time
            if uptime > timedelta(days=1):
                print(f"{host} is in Zabbix maintenance mode and has been running for {uptime}. Please check.")

def main():
    zapi = ZabbixAPI(ZABBIX_SERVER)
    zapi.session.verify = False

    with zapi as zabbix:
        zabbix.login(ZABBIX_USERNAME, ZABBIX_PASSWORD)
        print("Connected to Zabbix API Version %s" % zabbix.api_version())

        hosts = get_zabbix_hosts(zabbix)
        lower_host_list = [host.lower() for host in hosts]

        usa1_hosts = [host for host in lower_host_list if 'usa1' in host]
        check_maintenance_mode(zabbix, USA1_REGION_NAME, usa1_hosts)

        europe1_hosts = [host for host in lower_host_list if 'europe1' in host]
        check_maintenance_mode(zabbix, EUROPE1_REGION_NAME, europe1_hosts)

        if not usa1_hosts and not europe1_hosts:
            print("No servers in Zabbix maintenance mode that shouldn't be. Please close the ticket.")

if __name__ == '__main__':
    main()
