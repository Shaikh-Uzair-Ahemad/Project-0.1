from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import sqlite3


class AddStudent:
    def __init__(self, main):
        #  Create Database or Connection
        self.database = './MyDatabase/AttendanceDB.db'
        self.conn = sqlite3.connect(self.database)

        #  Main Window
        self.main = main
        self.main.state('zoomed')
        self.main.geometry("600x600")
        self.main.configure(bg='#FFFFFF')

        #  Main Frame
        self.main_frame = Frame(self.main, bg='white')
        self.main_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5), pady=5)

        # Student Information Frame
        self.frm_add_student = Frame(self.main_frame, bg='#EEEEEE')
        self.frm_add_student.pack(side=TOP, pady=50)

        #  Student Name
        self.lbl_Student_Name = Label(self.frm_add_student, text='Student Name')
        self.lbl_Student_Name.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.name_text = StringVar()
        self.student_name = Entry(self.frm_add_student, textvariable=self.name_text)
        self.student_name.grid(row=0, column=1, columnspan=3, sticky=EW, padx=(0, 10), pady=10)

        #  Student Roll No.
        self.lbl_Student_roll_no = Label(self.frm_add_student, text='Student Roll No.')
        self.lbl_Student_roll_no.grid(row=1, column=0, sticky=W, padx=10, pady=(0, 10))

        self.roll_no_text = StringVar()
        self.student_roll_no = Entry(self.frm_add_student, textvariable=self.roll_no_text)
        self.student_roll_no.grid(row=1, column=1, sticky=W, padx=(0, 10), pady=(0, 10))

        #  Upload Student Image
        self.lbl_upload_img = Label(self.frm_add_student, text='Upload Image')
        self.lbl_upload_img.grid(row=2, column=0, sticky=W, padx=10, pady=(0, 10))

        self.btn_upload_img = Button(self.frm_add_student, text='Upload Image', command=lambda: self.upload_img())
        self.btn_upload_img.grid(row=2, column=1, columnspan=2, sticky=EW, padx=(0, 10), pady=(0, 10))

        #  Show Image
        self.lbl_show_img = Label(self.frm_add_student, text='Image Preview', height=20)
        self.lbl_show_img.grid(row=3, column=0, columnspan=3, sticky=EW, padx=10, pady=(0, 10))

        #  Save Button
        self.btn_save = Button(self.frm_add_student, text='Save', width=10, command=lambda: self.add())
        self.btn_save.grid(row=4, column=2, sticky=E, padx=(0, 10), pady=(0, 10))

        #  Reset Button
        self.btn_reset = Button(self.frm_add_student, text='Reset', width=10, command=lambda: self.reset())
        self.btn_reset.grid(row=4, column=1, sticky=E, padx=10, pady=(0, 10))

    #  Upload Image Code
    def upload_img(self):
        try:
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                                       filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
            self.img = ImageTk.PhotoImage(Image.open(self.filename))  # Read the Image
            self.lbl_show_img.configure(image=self.img, height=300, width=300)

        except AttributeError:
            messagebox.showinfo('File Not Selected', 'Select An Image')

    #  Create Table
    def create_table(self):
        cursor = self.conn.cursor()
        try:
            #  Create Table Command
            create_table = """CREATE TABLE IF NOT EXISTS Students (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Name TEXT NOT NULL,
                            Roll_No INTEGER NOT NULL,
                            Image BLOB NOT NULL);"""

            #  Execute Command
            cursor.execute(create_table)
            self.conn.commit()

        except sqlite3.Error as e:
            print(e)

    def insert(self):
        #  Create Instance to Store Input Data
        student_name = self.name_text.get().title()
        student_roll = self.roll_no_text.get()
        with open(self.filename, 'rb') as file:
            img = file.read()

        cursor = self.conn.cursor()
        try:
            #  Check Roll No. Exists
            cursor.execute("SELECT * FROM Students WHERE Roll_No = ?", student_roll)
            row = cursor.fetchone()

            if row != None:
                messagebox.showinfo("Message", "Roll No. Already Exist")
            else:
                #  Insert Value into Table
                insert = """INSERT INTO Students(Name, Roll_No, Image) VALUES(?, ?, ?)"""

                #  Execute Command
                cursor.execute(insert, (student_name, student_roll, img))
                print('Record Successfully Inserted')
                self.conn.commit()

        except sqlite3.Error as e:
            print(e)

    #  Add Student Information
    def add(self):
        try:
            if self.name_text.get() == '' and self.roll_no_text.get() == '':
                messagebox.showwarning("Something went wrong", "Empty Filed Not Allowed")
            else:
                self.create_table()
                self.insert()
                messagebox.showinfo("Message", "Record Successfully Inserted")
                self.reset()

        except sqlite3.Error as e:
            print(e)
            messagebox.showwarning("Something went wrong", "Empty Filed Not Allowed")

    def reset(self):
        self.student_name.delete(0, END)
        self.student_name.focus()
        self.student_roll_no.delete(0, END)
        self.lbl_show_img.destroy()
        self.lbl_show_img = Label(self.frm_add_student, text='Image Preview', height=20)
        self.lbl_show_img.grid(row=3, column=0, columnspan=3, sticky=EW, padx=10, pady=(0, 10))


if __name__ == '__main__':
    root = Tk()
    obj = AddStudent(root)
    root.mainloop()
