from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml

from config import username, password

""" 
On device must be configured NetConf:
set system services netconf ssh
"""

hostname = '192.168.20.65'
junos_username = username
junos_password = password

yml_file = "routeStatus.yml"
globals().update(loadyaml(yml_file))

# login credentials required for SSH connection to console server
# cs_username = input("Console server username: ")
# cs_password = getpass("Console server password: ")

dev = Device(host=hostname, user=junos_username, passwd=junos_password)

print('Wait for connections')
dev.open()

print('Get Info')
tbl = RouteTable(dev)
tbl.get()
for key in tbl:
    print(key.name, key.via, key.to)

dev.close()
