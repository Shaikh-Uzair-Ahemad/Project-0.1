from tkinter import *
from tkinter import filedialog, messagebox
import sqlite3


class AddLecture:
    def __init__(self, main):
        # #  Create Database or Connection
        # self.database = './MyDatabase/LectureDB.db'
        # self.conn = sqlite3.connect(self.database)

        #  Main Window
        self.main = main
        self.main.state('zoomed')
        self.main.geometry("600x600")
        self.main.configure(bg='#FFFFFF')

        #  Main Frame
        self.main_frame = Frame(self.main, bg='white')
        self.main_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5), pady=5)

        # Student Information Frame
        self.frm_add_lecture = Frame(self.main_frame, bg='#EEEEEE')
        self.frm_add_lecture.pack(side=TOP, pady=50)

        #  Teacher Name
        self.lbl_Teacher_Name = Label(self.frm_add_lecture, text='Teacher Name')
        self.lbl_Teacher_Name.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.name_text = StringVar()
        self.teacher_name = Entry(self.frm_add_lecture, textvariable=self.name_text)
        self.teacher_name.grid(row=0, column=1, columnspan=3, sticky=EW, padx=(0, 10), pady=10)

        #  Lecture
        self.lbl_Lecture = Label(self.frm_add_lecture, text='Subject')
        self.lbl_Lecture.grid(row=1, column=0, sticky=W, padx=10, pady=(0, 10))

        self.lecture_text = StringVar()
        self.lecture_name = Entry(self.frm_add_lecture, textvariable=self.lecture_text)
        self.lecture_name.grid(row=1, column=1, columnspan=3, sticky=EW, padx=(0, 10), pady=(0, 10))

        #  Save Button
        self.btn_save = Button(self.frm_add_lecture, text='Save', width=10, command=lambda: self.add())
        self.btn_save.grid(row=4, column=2, sticky=E, padx=(0, 10), pady=(0, 10))

        #  Reset Button
        self.btn_reset = Button(self.frm_add_lecture, text='Reset', width=10, command=lambda: self.reset())
        self.btn_reset.grid(row=4, column=1, sticky=E, padx=10, pady=(0, 10))

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
        teacher_name = self.name_text.get().title()
        lecture_name = self.lecture_text.get()
        with open(self.filename, 'rb') as file:
            file.read()

        cursor = self.conn.cursor()
        try:
            #  Check Roll No. Exists
            cursor.execute("SELECT * FROM Lectures WHERE Lecture = ?", lecture_name)
            row = cursor.fetchone()

            if row is not None:
                messagebox.showinfo("Message", "Lecture  Already Exist")
            else:
                #  Insert Value into Table
                insert = """INSERT INTO Lectures(Teacher, Lecture_name) VALUES(?, ?)"""

                #  Execute Command
                cursor.execute(insert, (teacher_name, lecture_name))
                print('Record Successfully Inserted')
                self.conn.commit()

        except sqlite3.Error as e:
            print(e)

    #  Add Lecturer Information
    def add(self):
        try:
            if self.name_text.get() == '' and self.lecture_text.get() == '':
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
        self.teacher_name.delete(0, END)
        self.teacher_name.focus()
        self.lecture_name.delete(0, END)
        self.lecture_name.focus()


if __name__ == '__main__':
    root = Tk()
    obj = AddLecture(root)
    root.mainloop()
