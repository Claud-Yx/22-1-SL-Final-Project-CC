import tkinter.font
from tkinter import *
from tkinter.ttk import *

DAY_OF_WEEK = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

class DateButton(Frame):
    def __init__(self, master, date, month, running_count=None, deadline_count=None, data=dict, **kw):
        super().__init__(master, **kw)
        self.configure(relief=RAISED, border=1, padding=1)

        self.dayofweek = None
        self.month = IntVar(value=month)
        self.date = IntVar(value=date)
        self.running_count = IntVar(value=running_count)
        self.deadline_count = IntVar(value=deadline_count)

        self.date_font = tkinter.font.Font(size=10, weight='bold')

        self.date_frame = Frame(self)
        self.info_frame = Frame(self)
        self.date_frame.pack()
        self.info_frame.pack()

        self.date_label = Label(self.date_frame, textvariable=self.date, width=7, font=self.date_font)
        self.running_info = Label(self.info_frame, textvariable=self.deadline_count, width=7, anchor=E, foreground='green')
        self.deadline_info = Label(self.info_frame, textvariable=self.deadline_count, width=7, anchor=E, foreground='red')

        self.date_label.pack()
        self.running_info.pack()
        self.deadline_info.pack()

        self.date_label.bind('<Button-1>', self.pressed)
        self.date_label.bind('<ButtonRelease-1>', self.released)
        self.running_info.bind('<Button-1>', self.pressed)
        self.running_info.bind('<ButtonRelease-1>', self.released)
        self.deadline_info.bind('<Button-1>', self.pressed)
        self.deadline_info.bind('<ButtonRelease-1>', self.released)

    def pressed(self, event=NONE):
        self.configure(relief=SUNKEN)

    def released(self, event=NONE):
        self.configure(relief=RAISED)

    def date_color(self, color):
        self.date_label.configure(foreground=color)

    def disable(self):
        self.configure(relief=GROOVE)
        self.date_label.configure(foreground='gray')
        self.running_info.configure(text="")
        self.deadline_info.configure(text="")

        def f(event=None):
            pass

        self.date_label.bind("<Button-1>", f)
        self.date_label.bind("<ButtonRelease-1>", f)
        self.running_info.bind("<Button-1>", f)
        self.running_info.bind("<ButtonRelease-1>", f)
        self.deadline_info.bind("<Button-1>", f)
        self.deadline_info.bind("<ButtonRelease-1>", f)

    def release_bind(self, fn):
        def new_release(event=None):
            self.configure(relief=RAISED)
            fn(event)

        self.date_label.bind("<ButtonRelease-1>", new_release)
        self.running_info.bind("<ButtonRelease-1>", new_release)
        self.deadline_info.bind("<ButtonRelease-1>", new_release)

    def set_dayofweek(self, day):
        assert day in DAY_OF_WEEK, print(f"DAY OF WEEK error: {day}")
        self.dayofweek = day


if __name__ == '__main__':
    print("date_button module test start")
    window = Tk()
    window.attributes('-topmost', True)
    def destroy(event=None):
        window.quit()
    window.bind("<Escape>", destroy)
    line1 = Frame(window)
    line2 = Frame(window)

    line1.pack(padx=5)
    line2.pack(padx=5)

    date1 = DateButton(line1, 1, 6, running_count=5)
    date2 = DateButton(line1, 2, 6, running_count=152)
    date3 = DateButton(line2, 3, 6, running_count=12, deadline_count=2)
    date4 = DateButton(line2, 4, 6)

    date1.date_color('red')
    date3.date_color('blue')

    def print_test(event=None):
        print("binding test")

    date3.release_bind(print_test)
    date2.disable()

    date1.pack(side=LEFT)
    date2.pack(side=LEFT)
    date3.pack(side=LEFT)
    date4.pack(side=LEFT)

    window.mainloop()


