
"""
yml
"""
from multiprocessing.dummy import Process, Pool
import time
from timeit import Timer
import os

from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
from config import username, password, SRXAddresses


class SomeData:
    def __init__(self, name, address, un, passw):
        self.yml_file = "routeStatus.yml"
        globals().update(loadyaml(self.yml_file))
        self.dev = Device(host=address, user=un, passwd=passw)
        self.name = name
        self.version = ''
        self.address = address

        self.param = os.getpid()
        self.param2 = 0

    def uppdate_param(self):
        self.param2 += 1000

    def print_th(self):
        self.param2 = (os.getpid())


def update_in_pool(coll):
    pool1 = Pool()
    result = pool1.map(worker, coll)
    pool1.close()
    pool1.join()
    return result


def gen_list(pss):
    time.sleep(2)
    # print(pss[0], pss[1])
    sd = SomeData(pss[0], pss[1], username, password)
    sd.uppdate_param()
    # sd.uppdate_param()
    return sd


def update_data(qq, wp: SomeData):
    wp.print_th()
    print(wp)
    qq.put(wp)


collect = [['First', '192.168.0.50'],
           ['Second', '192.168.0.51'],
           ['Third', '192.168.0.52'],
           ['Fourth', '192.168.0.53'],
           ['Fifth', '192.168.0.54']]
arr = []


def main():
    pool = Pool()
    results = pool.map(gen_list, collect)

    for r in results:
        print(r.name, r.address, r.param, r.param2)

if __name__ == "__main__":

    # processes = [
    #     Process(target=gen_list, args=(q, name, adr, username, password,))
    #     for name, adr in SRXAddresses.items()
    # ]
    main()


    # for p in processes:
    #     p.start()
    # for p in processes:
    #     p.join()





