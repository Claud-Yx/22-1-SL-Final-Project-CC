import tkinter.font
from tkinter import *
from tkinter.ttk import *

from requests import delete

WEEKDAY = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
SELECTED_COLOR = '#d4ff00'

class DateButton(Frame):
    def __init__(self, master, date=None, month=None, weekday=None, running_count=None, deadline_count=None, data=dict, **kw):
        super().__init__(master, **kw)
        self.configure(relief=RAISED, border=1, padding=1)

        self.dayofweek = StringVar()
        self.new_fn = self.released

        self.delete_text = StringVar(value="")
        self.month = IntVar(value=month)
        self.date = IntVar(value=date)
        self.running_count = IntVar(value=running_count)
        self.deadline_count = IntVar(value=deadline_count)

        self.date_font = tkinter.font.Font(size=10, weight='bold')

        self.date_frame = Frame(self)
        self.info_frame = Frame(self)
        self.date_frame.pack()
        self.info_frame.pack()

        self.date_label = Label(self.date_frame, textvariable=self.date, width=9, font=self.date_font)
        self.running_info = Label(self.info_frame, textvariable=self.deadline_count, width=9, anchor=E, foreground='green')
        self.deadline_info = Label(self.info_frame, textvariable=self.deadline_count, width=9, anchor=E, foreground='red')

        if weekday:
            self.set_weekday(weekday)

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
        self.hide_info()

        def f(event=None):
            pass

        self.date_label.bind("<Button-1>", f)
        self.date_label.bind("<ButtonRelease-1>", f)
        self.running_info.bind("<Button-1>", f)
        self.running_info.bind("<ButtonRelease-1>", f)
        self.deadline_info.bind("<Button-1>", f)
        self.deadline_info.bind("<ButtonRelease-1>", f)

    def enable(self):
        self.configure(relief=RAISED)

        if self.dayofweek.get() == 'sun':
            self.date_label.configure(foreground='red')
        elif self.dayofweek.get() == 'sat':
            self.date_label.configure(foreground='blue')
        else:
            self.date_label.configure(foreground='black')

        self.show_info()

        self.date_label.bind("<Button-1>", self.pressed)
        self.date_label.bind("<ButtonRelease-1>", self.new_fn)
        self.running_info.bind("<Button-1>", self.pressed)
        self.running_info.bind("<ButtonRelease-1>", self.new_fn)
        self.deadline_info.bind("<Button-1>", self.pressed)
        self.deadline_info.bind("<ButtonRelease-1>", self.new_fn)

    def selected(self):
        self.date_label.configure(background=SELECTED_COLOR)
        self.running_info.configure(background=SELECTED_COLOR)
        self.deadline_info.configure(background=SELECTED_COLOR)

    def unselected(self):
        self.date_label.configure(background='SystemButtonFace')
        self.running_info.configure(background='SystemButtonFace')
        self.deadline_info.configure(background='SystemButtonFace')

    def show_info(self, mode='both'):
        if mode == 'ri':
            self.running_info.configure(textvariable=self.running_count)
        elif mode == 'di':
            self.deadline_info.configure(textvariable=self.deadline_count)
        elif mode == 'both':
            self.running_info.configure(textvariable=self.running_count)
            self.deadline_info.configure(textvariable=self.deadline_count)
        else:
            assert mode, print(f"MODE KEYWORD ERROR: {mode}")

    def hide_info(self, mode='both'):
        if mode == 'ri':
            self.running_info.configure(textvariable=self.delete_text)
        elif mode == 'di':
            self.deadline_info.configure(textvariable=self.delete_text)
        elif mode == 'both':
            self.running_info.configure(textvariable=self.delete_text)
            self.deadline_info.configure(textvariable=self.delete_text)
        else:
            assert mode, print(f"MODE KEYWORD ERROR: {mode}")

    def release_bind(self, fn):
        def new_release(event=None):
            self.configure(relief=RAISED)
            fn(event)

        self.new_fn = new_release

        self.date_label.bind("<ButtonRelease-1>", new_release)
        self.running_info.bind("<ButtonRelease-1>", new_release)
        self.deadline_info.bind("<ButtonRelease-1>", new_release)

    def set_weekday(self, day):
        assert day in WEEKDAY, print(f"DAY OF WEEK error: {day}")
        self.dayofweek.set(day)

        if day == 'sun':
            self.date_label.configure(foreground='red')
        elif day == 'sat':
            self.date_label.configure(foreground='blue')
        else:
            self.date_label.configure(foreground='black')



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

    date1 = DateButton(line1, 1, 6, 'sun', running_count=5)
    date2 = DateButton(line1, 2, 6, 'sat', running_count=152)
    date3 = DateButton(line2, 3, 6, 'sat', running_count=12, deadline_count=2)
    date4 = DateButton(line2, 4, 6, 'mon')

    def disable_date2(event=None):
        date2.disable()

    date2.release_bind(disable_date2)

    def print_test(event=None):
        print("binding test")

    date3.release_bind(print_test)
    date2.disable()

    def enable_date2(event=None):
        date2.enable()

    date4.release_bind(enable_date2)

    date1.pack(side=LEFT)
    date2.pack(side=LEFT)
    date3.pack(side=LEFT)
    date4.pack(side=LEFT)

    date1.selected()
    date3.unselected()

    window.mainloop()


