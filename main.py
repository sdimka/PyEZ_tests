from pprint import pprint
from jnpr.junos import Device

from config import username, password


hostname = '192.168.5.1'
junos_username = username
junos_password = password

# login credentials required for SSH connection to console server
# cs_username = input("Console server username: ")
# cs_password = getpass("Console server password: ")

dev = Device(host=hostname, user=junos_username, passwd=junos_password)
dev.open()

pprint(dev.facts)

# tbl = STPI

dev.close()
