from tkinter import *
from tkinter import font

from PIL import ImageTk, Image
import CreateFile
from datetime import datetime
import face_recognition
import numpy as np
import cv2
import os


class Attendance:
    def __init__(self, main):
        self.main = main
        self.main.state('zoomed')
        self.main.geometry("600x600")
        self.main.configure(bg='#FFFFFF')

        #  GUI for Video
        self.frm_video = Frame(self.main)
        self.frm_video.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5), pady=5)

        self.lbl_video = Label(self.frm_video, text='Click on Start Button to Launch Attendance')
        self.lbl_video.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        #  Frame for Buttons
        self.frm_btn = Frame(self.frm_video)
        self.frm_btn.pack(side=TOP, fill=X, padx=10, pady=10)

        self.btn_stop = Button(self.frm_btn, text='STOP')
        self.btn_stop.pack(side=RIGHT, padx=10, pady=10)
        self.custom_button(self.btn_stop)

        self.btn_start = Button(self.frm_btn, text='START', command=self.launch_camera)
        self.btn_start.pack(side=RIGHT, padx=10, pady=10)
        self.custom_button(self.btn_start)

    def launch_camera(self):
        #  Importing Images
        path = 'imgAttendance'
        images = []  # LIST CONTAINING ALL THE IMAGES
        class_name = []  # LIST CONTAINING ALL THE CORRESPONDING CLASS Names
        my_list = os.listdir(path)
        print("Total Classes Detected:", len(my_list))
        for x, cl in enumerate(my_list):
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            class_name.append(os.path.splitext(cl)[0])

        encode_list_known = self.find_encodings(images)
        print('Encodings Complete')

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        #  Webcam Image
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img_s = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

            #  Webcam Encodings
            faces_cur_frame = face_recognition.face_locations(img_s)
            encodes_cur_frame = face_recognition.face_encodings(img_s, faces_cur_frame)

            #  Find Matches
            for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
                matches = face_recognition.compare_faces(encode_list_known, encodeFace)
                face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
                match_index = np.argmin(face_dis)

                if matches[match_index]:
                    name = class_name[match_index].upper()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
                    self.mark_attendance(name)
                else:
                    name = 'Unknown Person'
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(img))
            self.lbl_video.configure(image=img)
            self.main.update()
            cv2.waitKey(1)

    def stop_camera(self):
        pass

    #  Compute Encodings
    @staticmethod
    def find_encodings(images):
        encode_list = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        return encode_list

    #  Making Attendance
    @staticmethod
    def mark_attendance(name):
        now = datetime.now()
        dtd_string = now.strftime("%d-%b-%Y")
        dtt_string = now.strftime("%I:%M:%S %p")

        #  Convert Object to String
        str_date = str(dtd_string)
        file_name = './Attendance/' + str_date + '.csv'

        if os.path.isfile(file_name):
            print('The file is updating...')
            with open(file_name, 'r+') as f:
                my_data_list = f.readlines()
                name_list = []
                for line in my_data_list:
                    entry = line.split(',')
                    name_list.append(entry[0])
                if name not in line:
                    f.write(f'\n{name},{dtt_string},{dtd_string}')
        else:
            CreateFile.CreateFile(file_name)
            print('The file is Created!')

    @staticmethod
    def custom_button(widget):
        btn_font = font.Font(family='bahnschrift condensed', size=18, weight='bold')
        widget.configure(width=10, bd=0, bg='#03051E', fg='#FFFFFF', activebackground='#E85D04',
                         activeforeground='#FFFFFF', font=btn_font)


if __name__ == '__main__':
    root = Tk()
    obj = Attendance(root)
    root = mainloop()
