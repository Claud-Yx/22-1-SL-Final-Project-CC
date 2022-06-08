import date_button as db
import month_button as mb
import tkinter.font
import calendar as cal
from tkinter import *
from tkinter.ttk import *

class Calendar(Frame):
    def __init__(self, master, date_data, **kw):
        super().__init__(master, **kw)
        self.configure(relief=GROOVE, border=20, padding=1)

        self.year = IntVar(value=date_data['year'])
        self.month = IntVar(value=date_data['month'])
        self.date = IntVar(value=date_data['date'])

        self.cur_month = [i for i in cal.Calendar(firstweekday=6).itermonthdays4(self.year.get(), self.month.get())]

        self.month_button = mb.MonthButton(self, self.year.get(), self.month.get())
        self.month_button.pack()

        self.dates_frame = Frame(self)

        self.week_frames = tuple(
            Frame(self.dates_frame) for i in range(5)
        )

        self.dates = tuple(tuple(db.DateButton(self.week_frames[j]) for i in range(7)) for j in range(5))

        for wf in self.week_frames:
            wf.pack()

        for i, w in enumerate(self.dates):
            for j, d in enumerate(w):
                cm = self.cur_month[i * 7 + j]
                d.month.set(cm[1])
                d.date.set(cm[2])
                d.set_dayofweek(db.DAY_OF_WEEK[cm[3]])
                d.pack(side=LEFT)

        self.dates_frame.pack(anchor=CENTER)


if __name__ == '__main__':
    print("calendar_gui module test start")
    window = Tk()
    window.title("calendar gui test")
    window.attributes('-topmost', True)


    def destroy(event=None):
        window.quit()

    window.bind("<Escape>", destroy)

    # 테스트 코드 부분을 적으시오.
    data = {'year': 2022, 'month': 6, 'date': 8}
    c = Calendar(window, data)
    c.pack()

    window.mainloop()
