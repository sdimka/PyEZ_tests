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

        self.devices = []
        for name, adr in SRXAddresses:
            dev = SRXdev.SRXDevice(name, adr, username, password)
            sub_fr = Window.SubFrame(self.main_window, name, adr, 'par2')
            action_with_arg = partial(self.connect_device, dev, sub_fr)
            sub_fr.abtn.config(command=action_with_arg)
            self.devices.append([dev, sub_fr])

        process = Process(target=self.check_status, args=())
        process.start()

    def do_something(self):
        for dev, fr in self.devices:
            print(dev.name)
        print('I do')

    def connect_device(self, dev, fr):
        fr.event_generate('<<UpdateStart>>', when='tail')
        # dev.fake_connect(fr)
        process = Process(target=dev.connect, args=(fr,))
        process.start()

    def check_status(self):
        for dev, fr in self.devices:
            if dev.lastState != dev.get_status():
                if dev.lastState:
                    fr.setBad()
                else:
                    fr.setGood()
                dev.lastState = dev.get_status()
        print('Recheck complete')
        for i in range(10, 0, -1):
            self.main_window.timeToUpdate.set(i)
            if self.active:
                time.sleep(1)

        # ToDo Problems with program end. Maybe this is not best solution
        if self.active:
            self.check_status()



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
