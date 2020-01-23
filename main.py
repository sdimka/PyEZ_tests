from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml

from config import username, password, SRXAddresses

""" 
On device must be configured NetConf:
set system services netconf ssh
"""


class SRXDevice():
    def __init__(self, address, un, passw):
        self.yml_file = "routeStatus.yml"
        globals().update(loadyaml(self.yml_file))
        self.dev = Device(host=address, user=un, passwd=passw)

    def connect(self):
        print('Wait for connections')
        self.dev.open()

    def get_route(self):
        tbl = RouteTable(self.dev)
        tbl.get('192.168.0.0/24')
        for key in tbl:
            print(key.name, key.via, key.to)

    def disconnect(self):
        print('Close connection')
        self.dev.close()


def main():

    devices = []
    for adr in SRXAddresses:
        devices.append(SRXDevice(adr, username, password))

    for dev in devices:
        dev.connect()

    print('Wait for input')
    x = int(input())

    for dev in devices:
        dev.get_route()

    for dev in devices:
        dev.disconnect()


if __name__ == '__main__':
    main()
