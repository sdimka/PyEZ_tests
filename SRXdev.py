from pprint import pprint
import time
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.exception import *
from multiprocessing.dummy import Process, Pool

from config import username, password, SRXAddresses

""" 
On device must be configured NetConf:
set system services netconf ssh
"""


class SRXDevice:
    def __init__(self, name, address, un, passw):
        self.yml_file = "routeStatus.yml"
        globals().update(loadyaml(self.yml_file))
        self.dev = Device(host=address, user=un, passwd=passw)
        self.name = name
        self.version = ''
        self.lastState = False
        self.lastError = ''

    def connect(self):
        print(self.name, 'wait for connections')
        try:
            self.dev.open()
        except ConnectRefusedError:
            print('Error: Connection refused!')
            return False
        except ConnectTimeoutError:
            print('Connection timeout error!')
            return False
        except ConnectUnknownHostError:
            print('Error: Connection attempt to unknown host')
            return False
        except ConnectionError:
            print('Connection error!')
            return False
        except ConnectAuthError:
            print('Connection authentication error!')
            return False
        else:
            print(self.name, 'connected!')
            return True


    def fake_connect(self):
        print('Begin fake connect')
        time.sleep(3)
        print('End fake connect')

    def get_route(self):
        tbl = RouteTable(self.dev)
        tbl.get('192.168.0.0/24')
        for key in tbl:
            result = key.to
            print(key.name, key.via, key.to)
        return result
        # fr.event_generate('<<UpdateStop>>', when='tail')

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

    def get_status(self):
        return self.dev.connected


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

    def sel_4(self):
        global selected_Dev, devices
        print(devices[selected_Dev].get_status())

    def dispatch(self, value):
        method_name = 'sel_' + str(value)
        method = getattr(self, method_name)
        return method()


def gen_list(n):
    sd = SRXDevice(n[0], n[1], username, password)
    sd.connect()
    sd.get_version()
    return sd


selected_Dev = 1
devices = []


def main():
    global selected_Dev, devices

    pool = Pool()
    devices = pool.map(gen_list, SRXAddresses)

    x = 1
    ch = Chooser()
    while x != 5:
        ch.dispatch(x)
        print('1 - Select device, 2 - Get info, 3 - Clear OSPF, 4 - Status, 5 - exit')
        x = int(input())

    # for dev in devices:
    #    dev.get_route()

    for dev in devices:
        dev.disconnect()


if __name__ == '__main__':
    #global selected_Dev, devices

    #for name, adr in SRXAddresses.items():
    #    devices.append(SRXDevice(name, adr, username, password))

    #for dev in devices:
    #    dev.connect()
    #    dev.get_version()

    main()
