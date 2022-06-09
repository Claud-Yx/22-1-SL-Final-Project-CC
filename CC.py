import calendar_gui as cg
import datetime as dt
from tkinter import *
from tkinter.ttk import *

CURRENT_DATE = dt.date.today()

window = Tk()
window.resizable(False, False)
window.geometry('+100+100')
window.title('Cultural Calendar')

# frame_1
frame_1 = Frame(window)
frame_1.pack(side=LEFT)

# 달력은 전시회 일정을 전체적으로 보여줌(해당 달에 있는 전시회가 몇 개인지만 표시)
calc = cg.Calendar(frame_1, {"year": CURRENT_DATE.year, "month": CURRENT_DATE.month, "date": CURRENT_DATE.day}, {})
calc.pack()

window.mainloop()



