#!/usr/bin/env python3

"""
Main window app
"""

from tkinter import Tk, Toplevel, Text, BOTH, W, N, E, S, X, Y, StringVar, PhotoImage
from tkinter.ttk import Frame, Button, Label, Style, Progressbar
from functools import partial


class SubFrame(Frame):
    def __init__(self, parent, name, param1, param2):
        super().__init__(parent)
        self.parent = parent

        self.name = name
        self.param1 = StringVar()
        self.param1.set(param1)
        self.param2 = param2
        self.status = False

        handler_start = partial(self.runProgress, message='Text')
        self.bind('<<UpdateStart>>', handler_start)
        handler_stop = partial(self.stopProgress)
        self.bind('<<UpdateStop>>', handler_stop)

        self.img_bad = PhotoImage(file='bad.png')
        self.img_good = PhotoImage(file='good.png')

        self.initUI()

    def initUI(self):
        self.pack(fill=X, expand=True)

        self['padding'] = (5, 10)
        self['borderwidth'] = 4
        self['relief'] = 'ridge'

        self.lbl0 = Label(self, image=self.img_bad)
        self.lbl0.image = self.img_bad
        self.lbl0.grid(row=0, column=0, sticky=W, pady=4, padx=5)

        lbl = Label(self, text=self.name)
        lbl.grid(row=0, column=1, sticky=W, pady=4, padx=5)

        self.lbl1 = Label(self, textvariable=self.param1, foreground="blue")
        self.lbl1.grid(row=0, column=2, sticky=W, pady=4, padx=5)

        lbl2 = Label(self, text=self.param2)
        lbl2.grid(row=0, column=3, sticky=W, pady=4, padx=5)

        self.abtn = Button(self, text="Connect")
        self.abtn.grid(row=1, column=0)

        self.bbtn = Button(self, text="Disconnect", command=self.onClick)
        self.bbtn.grid(row=1, column=1)

        cbtn = Button(self, text="Progress", command=self.runProgress)
        cbtn.grid(row=1, column=2, pady=4)

        self.pbar = Progressbar(self, mode='indeterminate')
        self.pbar.grid(row=2, column=0, columnspan=3, sticky=W + E)

    def onClick(self):
        self.setGood()
        # self.lbl0.config(image=self.img_good)
        # self.lbl0.image = self.img_good


    def runProgress(self, event, message):
        self.pbar.start()

    def stopProgress(self, event):
        self.pbar.stop()

    def setGood(self):
        self.lbl0.config(image=self.img_good)
        self.lbl0.image = self.img_good
        self.abtn.config(state="disabled")
        self.bbtn.config(state="normal")

    def setBad(self):
        self.lbl0.config(image=self.img_bad)
        self.lbl0.image = self.img_bad
        self.abtn.config(state="normal")
        self.bbtn.config(state="disabled")


class MainWindow(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        self.var = StringVar()
        self.var.set('Some text')

        self.timeToUpdate = StringVar()
        self.timeToUpdate.set('10')

        self.initUI()

    def initUI(self):

        self.title("Test app title")

        frame1 = Frame(self)
        frame1.pack(fill=X, expand=True)

        # frame1.columnconfigure(1, weight=1)
        # frame1.columnconfigure(3, pad=7)
        # frame1.rowconfigure(3, weight=1)
        # frame1.rowconfigure(5, pad=7)

        lbl = Label(frame1, textvariable=self.var)
        lbl.grid(row=0, column=0, sticky=W, pady=4, padx=5)

        lbl3 = Label(frame1, textvariable=self.timeToUpdate)
        lbl3.grid(row=0, column=3, sticky=W, pady=4, padx=5)

        self.abtn = Button(frame1, text="Activate")
        self.abtn.grid(row=1, column=3)

        self.btn_exit = Button(frame1, text="Close", command=self.onExit)
        self.btn_exit.grid(row=2, column=0, pady=4)

        self.hbtn = Button(frame1, text="Help")
        self.hbtn.grid(row=1, column=0, padx=5)

        self.obtn = Button(frame1, text="OK", command=self.onTestClick)
        self.obtn.grid(row=2, column=3)

        # frames = []
        # for i in range(1, 4):
        #     fr = SubFrame(self, f'Name {i}', 'Param1', 'Param2')
        #     fr.pack(fill=X, expand=True)
        #     frames.append(fr)



    def onExit(self):
        self.quit()

    def onTestClick(self):
        self.var.set('New text')


def main():
    root = Tk()
    #root.geometry("350x300+300+300")
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()