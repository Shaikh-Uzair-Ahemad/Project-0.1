from tkinter import *


class Home:
    def __init__(self, main):
        self.main = main
        self.frm_home = Frame(self.main, bg='blue')  # EEEEEE
        self.frm_home.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5), pady=5)


if __name__ == '__main__':
    root = Tk()
    obj = Home(root)
    root.mainloop()
