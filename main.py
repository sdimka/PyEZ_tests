from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
from jnpr.junos.utils.start_shell import StartShell

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
        self.name = ''
        self.version = ''

    def connect(self):
        print('Wait for connections')
        self.dev.open()

    def get_route(self):
        tbl = RouteTable(self.dev)
        tbl.get('192.168.0.0/24')
        for key in tbl:
            print(key.name, key.via, key.to)

    def clear_ospf(self):
        ss = StartShell(self.dev)
        ss.open()
        ss.run('cli -c "clear ospf neighbor area 0"')

    def get_version(self):
        ss = StartShell(self.dev)
        ss.open()
        self.version = ss.run('cli -c "show version"')

    def disconnect(self):
        print('Close connection')
        self.dev.close()


class Chooser:
    def sel_1(self):
        global selected_Dev, devices
        i = 0
        for dev in devices:
            print(i, dev.version)
            i += 1
        print('Select Device:')
        selected_Dev = int(input())

    def sel_2(self):
        global selected_Dev, devices
        devices[selected_Dev].get_route()

    def sel_3(self):
        global selected_Dev, devices
        devices[selected_Dev].clear_ospf()

    def dispatch(self, value):
        method_name = 'sel_' + str(value)
        method = getattr(self, method_name)
        return method()


selected_Dev = 1
devices = []


def main():
    global selected_Dev, devices

    for adr in SRXAddresses:
        devices.append(SRXDevice(adr, username, password))

    for dev in devices:
        dev.connect()
        dev.get_version()

    x = 1
    ch = Chooser()
    while x != 4:
        ch.dispatch(x)
        print('1 - Select device, 2 - Get info, 3 - Clear OSPF, 4 - exit')
        x = int(input())

    # for dev in devices:
    #    dev.get_route()

    for dev in devices:
        dev.disconnect()


if __name__ == '__main__':
    main()
