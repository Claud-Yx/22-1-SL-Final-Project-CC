from tkinter import *
from tkinter.ttk import *

calendar_window = Tk()
calendar_window.resizable(False, False)
calendar_window.geometry('+100+100')
calendar_window.title('Cultural Calendar')

# 달력은 전시회 일정을 전체적으로 보여줌(해당 달에 있는 전시회가 몇 개인지만 표시)
