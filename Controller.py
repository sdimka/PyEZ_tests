from tkinter import Tk, messagebox
from multiprocessing.dummy import Process
from functools import partial
import time
import Window
import SRXdev
from config import username, password, SRXAddresses


class Controller(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.active = True
        self.withdraw()

        self.main_window = Window.MainWindow(self)
        self.main_window.abtn.config(command=self.do_something)

        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_window.btn_exit.config(command=self.on_closing)
        self.main_window.abtn.config(command=self.connect_all)

        self.devices = []
        for name, adr in SRXAddresses:
            dev = SRXdev.SRXDevice(name, adr, username, password)
            sub_fr = Window.SubFrame(self.main_window, name, adr, '    N/A    ')
            action_with_arg = partial(self.connect_device, dev, sub_fr)
            sub_fr.abtn.config(command=action_with_arg)
            action1_with_arg = partial(self.get_curr_gw, dev, sub_fr)
            sub_fr.cbtn.config(command=action1_with_arg)
            action2_with_arg = partial(self.reset_ospf, dev, sub_fr)
            sub_fr.dbtn.config(command=action2_with_arg)
            sub_fr.setBad()
            self.devices.append([dev, sub_fr])

        process = Process(target=self.check_status, args=())
        process.start()

    def do_something(self):
        for dev, fr in self.devices:
            print(dev.name)
        print('I do')

    def dev_connect_tread(self, dev, fr):
        fr.event_generate('<<UpdateStart>>', when='tail')
        if dev.connect():
            # ToDo if connect success, update dev.lastSate here
            fr.param2.set(dev.get_route())
            dev.lastState = True
            fr.setGood()
        fr.event_generate('<<UpdateStop>>', when='tail')

    def connect_device(self, dev, fr):
        process = Process(target=self.dev_connect_tread, args=(dev, fr,))
        process.start()

    def get_curr_gw_thread(self, dev, fr):
        fr.event_generate('<<UpdateStart>>', when='tail')
        fr.param2.set(dev.get_route())
        fr.event_generate('<<UpdateStop>>', when='tail')

    def get_curr_gw(self, dev, fr):
        process = Process(target=self.get_curr_gw_thread, args=(dev, fr,))
        process.start()

    def reset_ospf_thread(self, dev, fr):
        fr.event_generate('<<UpdateStart>>', when='tail')
        dev.clear_ospf()
        time.sleep(15)
        fr.param2.set(dev.get_route())
        fr.event_generate('<<UpdateStop>>', when='tail')

    def reset_ospf(self, dev, fr):
        process = Process(target=self.reset_ospf_thread, args=(dev, fr,))
        process.start()

    def check_status(self):
        for dev, fr in self.devices:
            if dev.lastState != dev.get_status():
                if dev.lastState:
                    fr.setBad()
                else:
                    fr.setGood()
                dev.lastState = dev.get_status()
        for i in range(10, 0, -1):
            self.main_window.timeToUpdate.set(i)
            if self.active:
                time.sleep(1)
        if self.active:
            self.check_status()

    def connect_all(self):
        for dev, fr in self.devices:
            if not dev.lastState:
                process = Process(target=self.dev_connect_tread, args=(dev, fr,))
                process.start()


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.active = False
            for dev, fr in self.devices:
                if dev.get_status():
                    print(dev.name)
                    dev.disconnect()
            self.destroy()



if __name__ == '__main__':
    Controller().mainloop()
