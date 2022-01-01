from tkinter import messagebox, font
from tkinter.ttk import *
from tkinter import *
from PIL import ImageTk, Image
import csv
import os


class Report:
    def __init__(self, main):
        main_frame = Frame(main, bg='#EEEEEE')
        main_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5), pady=5)

        #  Get All Files Name From Directory
        self.file_name = './Attendance/'
        self.file_list = []
        for file in os.listdir(self.file_name):
            self.file_list.insert(0, os.path.splitext(file)[0])

        #  LabelFrame for Combobox and Button
        self.lbl_frm_cmb = LabelFrame(main_frame, text='Choose File')
        self.lbl_frm_cmb.pack(side=TOP, fill=X, padx=10, pady=10)

        self.combo_var = StringVar()
        self.cmb_list = Combobox(self.lbl_frm_cmb, values=self.file_list, textvariable=self.combo_var, width=50)
        self.cmb_list.pack(side=LEFT, padx=20, pady=20)
        self.cmb_list.set('Choose File...')

        self.btn_view = Button(self.lbl_frm_cmb, text='View', width=10)
        self.btn_view.pack(side=LEFT, padx=20, pady=20)
        self.btn_view.bind('<Button-1>', self.clicked)

        #  LabelFrame for TreeView
        self.lbl_frm_tree = LabelFrame(main_frame, text='Report View')
        self.lbl_frm_tree.pack(side=LEFT, fill=Y, padx=10, pady=10)

        self.frm_table = Frame(self.lbl_frm_tree)
        self.frm_table.pack(side=TOP, padx=20, pady=20)

        self.scroll_bar_x = Scrollbar(self.frm_table, orient=HORIZONTAL)
        self.scroll_bar_y = Scrollbar(self.frm_table, orient=VERTICAL)

        self.table_tree = Treeview(self.frm_table, columns=('Sr. No.', 'Name', 'Time', 'Date'), height=400,
                                   selectmode='extended', yscrollcommand=self.scroll_bar_y.set,
                                   xscrollcommand=self.scroll_bar_x.set)
        self.scroll_bar_y.config(command=self.table_tree.yview)
        self.scroll_bar_y.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x.config(command=self.table_tree.xview)
        self.scroll_bar_x.pack(side=BOTTOM, fill=X)

        self.table_tree.heading('Sr. No.', text='Sr. No.', anchor=CENTER)
        self.table_tree.heading('Name', text='Name', anchor=CENTER)
        self.table_tree.heading('Time', text='Time', anchor=CENTER)
        self.table_tree.heading('Date', text='Date', anchor=CENTER)

        self.table_tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.table_tree.column('#1', stretch=NO, minwidth=0, width=50, anchor=CENTER)
        self.table_tree.column('#2', stretch=NO, minwidth=0, width=300)
        self.table_tree.column('#3', stretch=NO, minwidth=0, width=150, anchor=CENTER)
        self.table_tree.column('#4', stretch=NO, minwidth=0, width=150, anchor=CENTER)
        self.table_tree.pack(side=TOP, fill=Y)
        self.table_tree.bind("<Button-1>", self.item_selected)

        #  LabelFrame for Image View
        self.lbl_frm_img = LabelFrame(main_frame, text='Image')
        self.lbl_frm_img.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        self.lbl_img = Label(self.lbl_frm_img, text='Click on Name to Show Image')
        self.lbl_img.pack(side=TOP, pady=(10, 0))

        self.lbl_img_name = Label(self.lbl_frm_img)
        self.lbl_img_name.pack(side=BOTTOM, pady=10)

    #  View Button Event Fire with Clicked Method
    def clicked(self, event):
        if self.combo_var.get() == 'Choose File...':
            messagebox.showinfo('Select File', 'Select File')
        else:
            self.table_tree.delete(*self.table_tree.get_children())
            file_name = self.combo_var.get()

            with open('./Attendance/' + file_name + '.csv') as f:
                reader = csv.DictReader(f, delimiter=',')
                count = 1
                for row in reader:
                    name = row['Name']
                    time = row['Time']
                    date = row['Date']
                    self.table_tree.insert("", 0, values=(count, name, time, date))
                    count = count + 1

    #  TreeView Item Selection Event Fire with item_selection Method
    def item_selected(self, event):
        for selected_item in self.table_tree.selection():
            item = self.table_tree.item(selected_item)
            record = item['values']
            name = record[1]

            self.img = ImageTk.PhotoImage(Image.open('./imgAttendance/' + name + '.jpg'))
            self.lbl_img.configure(image=self.img, height=400, width=300)

            lbl_font = font.Font(family='bahnschrift condensed', size=14)
            self.lbl_img_name.configure(text=name, font=lbl_font)


if __name__ == '__main__':
    root = Tk()
    obj = Report(root)
    root.mainloop()
