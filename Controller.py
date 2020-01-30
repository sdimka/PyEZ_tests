from tkinter import Tk, Toplevel, Label, Entry, Button, W, E
import Window


class Controller(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()

        self.main_window = Window.MainWindow(self)
        self.sw = Window.SubFrame(self.main_window, 'name', 'par1', 'par2')


if __name__ == '__main__':
    Controller().mainloop()
