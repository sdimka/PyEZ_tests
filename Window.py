#!/usr/bin/env python3

"""
Main window app
"""

from tkinter import Tk, Text, BOTH, W, N, E, S, X, Y, StringVar
from tkinter.ttk import Frame, Button, Label, Style, Progressbar


class SubFrame(Frame):
    def __init__(self, parent : Frame, name, param1, param2):
        super().__init__()
        self.parent = parent

        self.name = name
        self.param1 = StringVar()
        self.param1.set(param1)
        self.param2 = param2
        self.lbl1 = Label()
        self.status = False

        self.initUI()


    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        self['padding'] = (5, 10)
        self['borderwidth'] = 4
        self['relief'] = 'ridge'
        # style = Style()  # Create style
        # style.configure("Blue.TFrame", background="green")  # Set bg color
        # self.config(style='Blue.TFrame')  # Apply style to widget

        lbl = Label(self, text=self.name)
        lbl.grid(row=0, column=0, sticky=W, pady=4, padx=5)

        self.lbl1 = Label(self, textvariable=self.param1, foreground="blue")
        self.lbl1.grid(row=0, column=1, sticky=W, pady=4, padx=5)

        lbl2 = Label(self, text=self.param2)
        lbl2.grid(row=0, column=2, sticky=W, pady=4, padx=5)

        abtn = Button(self, text="Connect", command=self.onClick)
        abtn.grid(row=1, column=0)

        cbtn = Button(self, text="Progress", command=self.runProgress)
        cbtn.grid(row=1, column=1, pady=4)

        self.pbar = Progressbar(self, mode='indeterminate')
        self.pbar.grid(row=2, column=0, columnspan=3, sticky=W + E)

    def onClick(self):
        self.param1.set('New text')
        self.lbl1['foreground']='red'
        # self.lbl1.config(text='New text')
        # self.update_idletasks()

    def runProgress(self):
        if not self.status:
            self.pbar.start()
            self.status = True
        else:
            self.pbar.stop()
            self.status = False



class Example(Frame):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.var = StringVar()
        self.var.set('Some text')

        self.initUI()

    def initUI(self):

        self.parent.title("Test app title")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X, expand=True)

        # frame1.columnconfigure(1, weight=1)
        # frame1.columnconfigure(3, pad=7)
        # frame1.rowconfigure(3, weight=1)
        # frame1.rowconfigure(5, pad=7)

        lbl = Label(frame1, textvariable=self.var)
        lbl.grid(row=0, column=0, sticky=W, pady=4, padx=5)

        abtn = Button(frame1, text="Activate")
        abtn.grid(row=1, column=3)

        cbtn = Button(frame1, text="Close", command=self.onExit)
        cbtn.grid(row=2, column=0, pady=4)

        hbtn = Button(frame1, text="Help")
        hbtn.grid(row=1, column=0, padx=5)

        obtn = Button(frame1, text="OK", command=self.onTestClick)
        obtn.grid(row=2, column=3)

        frames = []
        for i in range(1, 4):
            fr = SubFrame(frame1, f'Name {i}', 'Param1', 'Param2')
            fr.pack(fill=X, expand=True)
            frames.append(fr)

    def onExit(self):
        self.quit()

    def onTestClick(self):
        self.var.set('New text')


def main():

    root = Tk()
    #root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()