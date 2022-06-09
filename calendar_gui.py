import date_button as db
import month_button as mb
import tkinter.font
import calendar as cal
from tkinter import *
from tkinter.ttk import *


# content data는 dict형태로 해당 전시회 이름, 시작 날짜, 종료 날짜 등의 key값이 존재

class Calendar(Frame):
    def __init__(self, master, date_data, content_data, **kw):
        super().__init__(master, **kw)
        self.configure(relief=GROOVE, border=2, padding=1)

        self.content_data = content_data

        self.year = IntVar(value=date_data['year'])
        self.month = IntVar(value=date_data['month'])
        self.date = IntVar(value=date_data['date'])

        self.cur_month_data = []
        self.refresh_month()

        self.month_button = mb.MonthButton(self, self.year.get(), self.month.get())
        self.month_button.pack(anchor=CENTER)

        def lbReleased(event, master=self.month_button.left_button):
            self.month_button.prev_month()
            self.month_button.refresh_year_month()
            self.year.set(self.month_button.year.get())
            self.month.set(self.month_button.month.get())
            self.refresh_calendar()
            return self.month_button.released(event, master)

        self.month_button.left_button.bind("<ButtonRelease-1>", lbReleased)

        def rbReleased(event, master=self.month_button.right_button):
            self.month_button.next_month()
            self.month_button.refresh_year_month()
            self.year.set(self.month_button.year.get())
            self.month.set(self.month_button.month.get())
            self.refresh_calendar()
            return self.month_button.released(event, master)

        self.month_button.right_button.bind("<ButtonRelease-1>", rbReleased)

        self.weekday_frame = Frame(self, padding=1)
        self.weekday_frame.pack(anchor=CENTER)

        self.weekday_font = tkinter.font.Font(size=10, weight='bold')
        self.weekday_attributes = tuple(
            Label(self.weekday_frame, text=db.WEEKDAY[i-1], width=9, relief=SOLID, border=1, padding=1,
                  font=self.weekday_font) for i in range(7)
        )

        for i, weekday in enumerate(self.weekday_attributes):
            if db.WEEKDAY[i-1] == db.WEEKDAY[5]:
                weekday.configure(foreground='blue')
            elif db.WEEKDAY[i-1] == db.WEEKDAY[6]:
                weekday.configure(foreground='red')
            else:
                weekday.configure(foreground='black')
            weekday.pack(side=LEFT, ipadx=1, padx=1, pady=1, anchor=CENTER)

        self.dates_frame = Frame(self)
        self.dates_frame.pack(anchor=CENTER)

        self.week_frames = tuple(
            Frame(self.dates_frame) for i in range(6)
        )

        self.dates = tuple(tuple(db.DateButton(self.week_frames[j]) for i in range(7)) for j in range(6))
        self.selected_date_frame = None

        for wf in self.week_frames:
            wf.pack(anchor=CENTER)

        self.refresh_dates()

    def refresh_dates(self):
        if self.selected_date_frame:
            self.selected_date_frame.unselected()

        def new_bind(event, selected_date):
            self.selected_date_frame.unselected()
            self.selected_date_frame = selected_date
            self.selected_date_frame.selected()
            self.date.set(selected_date.date.get())

        self.selected_date_frame = None

        first_date = None
        for i, w in enumerate(self.dates):
            for j, d in enumerate(w):
                cm = self.cur_month_data[i * 7 + j]
                d.enable()
                d.month.set(cm[1])
                d.date.set(cm[2])
                d.set_weekday(db.WEEKDAY[cm[3]])
                if d.date.get() == 1 and d.month.get() == self.month.get():
                    first_date = d
                if d.date.get() == self.date.get() and d.month.get() == self.month.get():
                    self.selected_date_frame = d

                def select_date(event, sd=d):
                    new_bind(event, sd)

                if not d.month.get() == self.month.get():
                    d.disable()
                else:
                    if d.running_count.get() == 0:
                        d.hide_info('ri')
                    if d.deadline_count.get() == 0:
                        d.hide_info('di')
                    d.release_bind(select_date)

                d.pack(side=LEFT, padx=1, pady=1, anchor=CENTER)

        if not self.selected_date_frame:
            self.selected_date_frame = first_date
            self.date.set(self.selected_date_frame.date.get())
        self.selected_date_frame.selected()

    def refresh_month(self):
        self.cur_month_data = [i for i in cal.Calendar(firstweekday=6).itermonthdays4(self.year.get(), self.month.get())]
        if self.cur_month_data.__len__() <= 35:
            self.cur_month_data += [d for i, d
                                    in enumerate(
                    cal.Calendar(firstweekday=6).itermonthdays4(
                        self.year.get(), self.month.get() + 1 if self.month.get() < 12 else 1))
                                    if 14 > i >= 7]

    def refresh_calendar(self):
        self.refresh_month()
        self.refresh_dates()



if __name__ == '__main__':
    print("calendar_gui module test start")
    window = Tk()
    window.title("calendar gui test")
    window.attributes('-topmost', True)


    def destroy(event=None):
        window.quit()

    window.bind("<Escape>", destroy)

    # 테스트 코드 부분을 적으시오.
    data = {'year': 2022, 'month': 6, 'date': 1}
    c = Calendar(window, data, {})
    c.pack()

    window.mainloop()
