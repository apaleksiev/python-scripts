#!/usr/bin/env python

from datetime import datetime, timedelta
import pytz
import boto3
from pyzabbix import ZabbixAPI
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ZABBIX_SERVER='https://zabbix.com/zabbix/api_jsonrpc.php'
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.session.verify = False
zapi.login('username','password')
print("Connected to Zabbix API Version %s" % zapi.api_version())

servers = zapi.host.get(groupids="24", output=['name'])
hostlst = []
for i in servers:
    hostlst.append(i['name'])
lower_host_list = [host.lower() for host in hostlst]

def main():
    for host in lower_host_list:
        if 'usa1' in host:
            ec2 = boto3.resource('ec2', region_name='us-east-1')
            filters = [
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': [host]}
            ]

            instances = ec2.instances.filter(Filters=filters)
            for i in instances:
                usa1_list = []
                uptime = datetime.now(pytz.utc) - i.launch_time
                if uptime > timedelta(days=1):
                    usa1_list.append({'Host': host, 'uptime': uptime})
                    print("%s is in Zabbix maintenance mode and has been running for %s. Please check." % (host, uptime))

        else:
            if 'europe1' in host:
                ec2 = boto3.resource('ec2', region_name='eu-west-1')
                filters = [
                    {'Name': 'instance-state-name', 'Values': ['running']},
                    {'Name': 'tag:Name', 'Values': [host]}
                ]

                instances = ec2.instances.filter(Filters=filters)
                for i in instances:
                    eur_list = []
                    uptime = datetime.now(pytz.utc) - i.launch_time
                    if uptime > timedelta(days=1):
                        eur_list.append({'Host': host, 'uptime': uptime})
                        print("%s is in Zabbix maintenance mode and has been running for %s. Please check." % (host, uptime))

    if (len(usa1_list) == 0) and (len(eur_list) == 0):
        print("No servers in Zabbix maintenance mode that shouldn't be. Please close the ticket.")

if __name__ == '__main__':
    main()
zapi.user.logout()