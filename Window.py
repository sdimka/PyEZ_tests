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
        self.param2 = StringVar()
        self.param2.set(param2)
        self.param3 = StringVar()
        # self.param3.set(param3)
        self.status = False

        handler_start = partial(self.runProgress, message='Text')
        self.bind('<<UpdateStart>>', handler_start)
        handler_stop = partial(self.stopProgress)
        self.bind('<<UpdateStop>>', handler_stop)

        self.img_bad = PhotoImage(file='bad.png')
        self.img_good = PhotoImage(file='good.png')
        self.img_err = PhotoImage(file='bad_conn.png')
        self.img_wrongGW = PhotoImage(file='error.png')

        self.initUI()

    def initUI(self):
        self.pack(fill=X, expand=True)

        self['padding'] = (5, 10)
        self['borderwidth'] = 4
        self['relief'] = 'ridge'

        self.lbl0 = Label(self, image=self.img_bad)
        self.lbl0.image = self.img_bad
        self.lbl0.grid(row=0, column=0, rowspan=2, sticky=W, pady=1, padx=5)

        lbl = Label(self, text=self.name)
        lbl.grid(row=0, column=1, sticky=W, pady=1, padx=5)

        self.lbl1a = Label(self, text='IP', foreground="blue", font='TkDefaultFont 12 bold')
        self.lbl1a.grid(row=0, column=2, sticky=N, pady=1, padx=5)

        self.lbl1 = Label(self, textvariable=self.param1, foreground="blue")
        self.lbl1.grid(row=1, column=2, sticky=W, pady=1, padx=5)

        self.lbl2a = Label(self, text='G/W', font='TkDefaultFont 12 bold')
        self.lbl2a.grid(row=0, column=3, sticky=N, pady=1, padx=5)

        self.lbl2 = Label(self, textvariable=self.param2)
        self.lbl2.grid(row=1, column=3, sticky=W, pady=1, padx=5)

        self.lbl3a = Label(self, text='Last error:', font='TkDefaultFont 12 bold')
        self.lbl3a.grid(row=0, column=4, sticky=N, pady=1, padx=5)

        self.lbl3 = Label(self, textvariable=self.param3)
        self.lbl3.grid(row=1, column=4, sticky=W, pady=1, padx=5)

        self.abtn = Button(self, text="Connect")
        self.abtn.grid(row=0, column=5)

        self.bbtn = Button(self, text="Disconnect", command=self.onClick)
        self.bbtn.grid(row=0, column=6)

        self.cbtn = Button(self, text="Get GW", command=self.runProgress)
        self.cbtn.grid(row=1, column=5, pady=4)

        self.dbtn = Button(self, text="Res OSPF", command=self.onClick)
        self.dbtn.grid(row=1, column=6, pady=4)

        self.pbar = Progressbar(self, mode='indeterminate')
        self.pbar.grid(row=1, column=1, sticky=W + E)  # columnspan=4

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
        self.cbtn.config(state="normal")
        self.dbtn.config(state="normal")

    def setBad(self):
        self.lbl0.config(image=self.img_bad)
        self.lbl0.image = self.img_bad
        self.abtn.config(state="normal")
        self.bbtn.config(state="disabled")
        self.cbtn.config(state="disabled")
        self.dbtn.config(state="disabled")

    def setError(self):
        self.lbl0.config(image=self.img_err)
        self.lbl0.image = self.img_err
        self.abtn.config(state="normal")
        self.bbtn.config(state="disabled")
        self.cbtn.config(state="disabled")
        self.dbtn.config(state="disabled")

    def setWrongGW(self):
        self.lbl0.config(image=self.img_wrongGW)
        self.lbl0.image = self.img_wrongGW
        self.abtn.config(state="disabled")
        self.bbtn.config(state="normal")
        self.cbtn.config(state="normal")
        self.dbtn.config(state="normal")


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

        self.abtn = Button(frame1, text='Connect all')
        self.abtn.grid(row=1, column=3)

        self.btn_exit = Button(frame1, text="Close", command=self.onExit)
        self.btn_exit.grid(row=1, column=4, pady=4)

        self.hbtn = Button(frame1, text="Help")
        self.hbtn.grid(row=1, column=0, padx=1)

        self.obtn = Button(frame1, text="OK", command=self.onTestClick)
        self.obtn.grid(row=1, column=2)

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