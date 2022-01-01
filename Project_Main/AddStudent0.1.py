from tkinter import *
from tkinter import filedialog, messagebox

import gridfs
from PIL import ImageTk, Image
import pymongo


class AddStudent:
    def __init__(self, main):
        my_client = pymongo.MongoClient('mongodb://localhost:27017/')
        my_db = my_client['attendanceDB']
        self.fs = gridfs.GridFS(my_db)
        my_collection = my_db['students']

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

        self.lbl_Student_Name = Label(self.frm_add_student, text='Student Name')
        self.lbl_Student_Name.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.name_text = StringVar()
        self.student_name = Entry(self.frm_add_student, textvariable=self.name_text)
        self.student_name.grid(row=0, column=1, columnspan=3, sticky=EW, padx=(0, 10), pady=10)

        self.lbl_Student_roll_no = Label(self.frm_add_student, text='Student Roll No.')
        self.lbl_Student_roll_no.grid(row=1, column=0, sticky=W, padx=10, pady=(0, 10))

        self.roll_no_text = StringVar()
        self.student_roll_no = Entry(self.frm_add_student, textvariable=self.roll_no_text)
        self.student_roll_no.grid(row=1, column=1, sticky=W, padx=(0, 10), pady=(0, 10))

        self.lbl_upload_img = Label(self.frm_add_student, text='Upload Image')
        self.lbl_upload_img.grid(row=2, column=0, sticky=W, padx=10, pady=(0, 10))

        self.btn_upload_img = Button(self.frm_add_student, text='Upload Image', command=lambda: self.upload_img())
        self.btn_upload_img.grid(row=2, column=1, columnspan=2, sticky=EW, padx=(0, 10), pady=(0, 10))

        self.lbl_show_img = Label(self.frm_add_student, text='Image Preview', height=20)
        self.lbl_show_img.grid(row=3, column=0, columnspan=3, sticky=EW, padx=10, pady=(0, 10))

        self.btn_save = Button(self.frm_add_student, text='Save', width=10, command=lambda: self.add())
        self.btn_save.grid(row=4, column=2, sticky=E, padx=(0, 10), pady=(0, 10))

        self.btn_reset = Button(self.frm_add_student, text='Reset', width=10)
        self.btn_reset.grid(row=4, column=1, sticky=E, padx=10, pady=(0, 10))

    def upload_img(self):
        try:
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select an Image", filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
            self.img = ImageTk.PhotoImage(Image.open(self.filename))  # Read the Image
            self.lbl_show_img.configure(image=self.img, height=300, width=300)

        except AttributeError:
            messagebox.showinfo('File Not Selected', 'Select An Image')

    def add(self):
        with open(self.filename, 'rb') as f:
            contents = f.read()
        self.fs.put(contents, filename='Test')


if __name__ == '__main__':
    root = Tk()
    obj = AddStudent(root)
    root.mainloop()
