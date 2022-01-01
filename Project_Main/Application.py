from tkinter import font, ttk
from tkinter.ttk import *
from tkinter import *

import Home
import Attendance
import Report


class AppGUI:
    def __init__(self, main):
        #  Main Window Configuration
        self.main = main
        self.main.title("Auto Attendance System")
        self.main.state('zoomed')
        self.main.geometry("600x400")
        self.main.configure(bg='#FFFFFF')

        #  Menu Buttons Icons
        self.icon_home = PhotoImage(file='./Icons/home_page.png')
        self.icon_attendance = PhotoImage(file='./Icons/attendance.png')
        self.icon_report = PhotoImage(file='./Icons/report.png')
        self.icon_add_member = PhotoImage(file='./Icons/add_member.png')
        self.icon_total_member = PhotoImage(file='./Icons/total_members.png')

        #  Call Frames
        self.menu_frames(self.main)

    def menu_frames(self, frame):
        #  Title Frame
        frm_title = Frame(frame, bg='#FF9800')
        frm_title.pack(side=TOP, fill=X)

        #  Title Text
        lbl_font = font.Font(family='Open Sans ExtraBold', size=30)
        lbl_title = Label(frm_title, text='Auto Attendance System', bg='#FF9800', fg='#FFFFFF', font=lbl_font)
        lbl_title.pack(side=LEFT, ipady=20, ipadx=20)

        # Menu Frame
        frm_menu = Frame(frame, bg='#03051E', width=250)
        frm_menu.pack(side=LEFT, fill=Y, padx=(0, 5), pady=5)

        #  Call Buttons
        self.menu_buttons(frm_menu)

    def menu_buttons(self, menu):
        #  Menu Buttons
        btn_home = Button(menu, image=self.icon_home, text=' Home', command=lambda: self.home_button(self.main))
        self.custom_button(btn_home)
        btn_home.pack(fill=X, ipady=5)
        btn_home.bind('<Enter>', self.button_hover)
        btn_home.bind('<Leave>', self.button_leave)

        btn_attendance = Button(menu, image=self.icon_attendance, text=' Attendance', command=lambda: self.attendance_button(self.main))
        self.custom_button(btn_attendance)
        btn_attendance.pack(fill=X, ipady=5)
        btn_attendance.bind('<Enter>', self.button_hover)
        btn_attendance.bind('<Leave>', self.button_leave)

        btn_report = Button(menu, image=self.icon_report, text=' Attendance Report', command=lambda: self.report_button(self.main))
        self.custom_button(btn_report)
        btn_report.pack(fill=X, ipady=5)
        btn_report.bind('<Enter>', self.button_hover)
        btn_report.bind('<Leave>', self.button_leave)

        btn_add_member = Button(menu, image=self.icon_add_member, text=' Add Member')
        self.custom_button(btn_add_member)
        btn_add_member.pack(fill=X, ipady=5)
        btn_add_member.bind('<Enter>', self.button_hover)
        btn_add_member.bind('<Leave>', self.button_leave)

        btn_total_member = Button(menu, image=self.icon_total_member, text=' Total Members')
        self.custom_button(btn_total_member)
        btn_total_member.pack(fill=X, ipady=5)
        btn_total_member.bind('<Enter>', self.button_hover)
        btn_total_member.bind('<Leave>', self.button_leave)

        #  Separator
        separator = ttk.Separator(menu, orient='horizontal')
        separator.pack(fill=X, padx=5)

    @staticmethod
    def home_button(main):
        Home.Home(main)

    @staticmethod
    def attendance_button(main):
        Attendance.Attendance(main)

    @staticmethod
    def report_button(main):
        Report.Report(main)




    #  Menu Buttons Configuration
    @staticmethod
    def custom_button(widget):
        btn_font = font.Font(family='bahnschrift condensed', size=18, weight='bold')
        widget.configure(width=250, anchor='w', bd=0, bg='#03051E', fg='#FFFFFF', activebackground='#E85D04',
                         activeforeground='#FFFFFF', compound=LEFT, font=btn_font)

    # Menu Buttons Hover Effect
    @staticmethod
    def button_hover(event):
        event.widget['bg'] = '#FF9800'

    @staticmethod
    def button_leave(event):
        event.widget['bg'] = '#03051E'


if __name__ == '__main__':
    root = Tk()
    obj = AppGUI(root)
    root.mainloop()
