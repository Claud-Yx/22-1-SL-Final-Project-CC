import tkinter.font
import date_button as db
from tkinter import *
from tkinter.ttk import *


class MonthButton(Frame):
    def __init__(self, master, year, month, data=dict, **kw):
        super().__init__(master, **kw)
        self.configure(relief=GROOVE, border=1, padding=1)

        self.year = IntVar(value=year)
        self.month = IntVar(value=month)
        self.year_month = StringVar(
            value=(str(self.year.get()) + "년 " + str(self.month.get()) + "월")
        )
        self.data = data

        self.month_font = tkinter.font.Font(size=20, weight='bold')
        self.button_font = tkinter.font.Font(size=40, weight='bold')

        self.month_label = Label(self, textvariable=self.year_month, cursor="hand2",
                                 width=25, anchor=CENTER, font=self.month_font)
        self.left_button = Label(self, text="◀", anchor=CENTER, relief=RAISED, font=self.button_font)
        self.right_button = Label(self, text="▶", anchor=CENTER, relief=RAISED, font=self.button_font)

        # packing
        self.left_button.pack(side=LEFT, ipadx=14, padx=1, pady=1)
        self.month_label.pack(side=LEFT, ipady=16)
        self.right_button.pack(side=LEFT, ipadx=15, padx=1, pady=1)

        # binding
        def lbPressed(event, master=self.left_button):
            return self.pressed(event, master)

        def lbReleased(event, master=self.left_button):
            self.prev_month()
            self.refresh_year_month()
            return self.released(event, master)

        self.left_button.bind('<Button-1>', lbPressed)
        self.left_button.bind('<ButtonRelease-1>', lbReleased)

        def rbPressed(event, master=self.right_button):
            return self.pressed(event, master)

        def rbReleased(event, master=self.right_button):
            self.next_month()
            self.refresh_year_month()
            return self.released(event, master)

        self.right_button.bind('<Button-1>', rbPressed)
        self.right_button.bind('<ButtonRelease-1>', rbReleased)

        def mPressed(event, master=self.month_label):
            return self.pressed(event, master)

        def mReleased(event, master=self.month_label):
            return self.released(event, master)

        self.month_label.bind('<Button-1>', mPressed)
        self.month_label.bind('<ButtonRelease-1>', mReleased)

    @staticmethod
    def pressed(event, master):
        master.configure(relief=SUNKEN)

    @staticmethod
    def released(event, master):
        if master['text'].__len__() < 2:
            master.configure(relief=RAISED)
        else:
            master.configure(relief=FLAT)

    @staticmethod
    def release_bind(master, fn):
        def new_release(event=None):
            if master['text'].__len__() < 2:
                master.configure(relief=RAISED)
            else:
                master.configure(relief=FLAT)
            fn(event)

        master.bind("<ButtonRelease-1>", new_release)

    def next_month(self):
        if self.month.get() == 12:
            self.month.set(1)
            self.year.set(self.year.get() + 1)
        else:
            self.month.set(self.month.get() + 1)

    def prev_month(self):
        if self.month.get() == 1:
            self.month.set(12)
            self.year.set(self.year.get() - 1)
        else:
            self.month.set(self.month.get() - 1)

    def next_year(self):
        self.year.set(self.year.get() + 1)

    def prev_year(self):
        self.year.set(self.year.get() - 1)

    def refresh_year_month(self):
        self.year_month.set(
            (str(self.year.get()) + "년 " + str(self.month.get()) + "월")
        )


if __name__ == '__main__':
    print("month_button module test start")
    window = Tk()
    window.title("monthButton test")
    window.attributes('-topmost', True)


    def destroy(event=None):
        window.quit()

    window.bind("<Escape>", destroy)

    # 테스트 코드 부분을 적으시오.
    month = MonthButton(window, 2022, 6)
    month.pack()

    # month.release_bind(month.left_button, lambda event: print("left button pressed"))
    # month.release_bind(month.right_button, lambda event: print("right button pressed"))
    month.release_bind(month.month_label, lambda event: print("month label pressed"))

    window.mainloop()
