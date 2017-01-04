from DataObjects import  *

# 1.) Create a track with example data
track = TimeTrack("TestTrack")

track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 8, 15), datetime(2016, 12, 30, 12, 30), "Planning architecture"))
track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 13, 00), datetime(2016, 12, 30, 18, 30), "Implementing"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 10, 00), datetime(2017, 1, 1, 16, 30), "Fixing stuff"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 20, 00), datetime(2017, 1, 1, 22, 10), "more fixing"))
track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 8, 15), datetime(2016, 12, 30, 12, 30), "Planning architecture"))
track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 13, 00), datetime(2016, 12, 30, 18, 30), "Implementing"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 10, 00), datetime(2017, 1, 1, 16, 30), "Fixing stuff"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 20, 00), datetime(2017, 1, 1, 22, 10), "more fixing"))
track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 8, 15), datetime(2016, 12, 30, 12, 30), "Planning architecture"))
track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 13, 00), datetime(2016, 12, 30, 18, 30), "Implementing"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 10, 00), datetime(2017, 1, 1, 16, 30), "Fixing stuff"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 20, 00), datetime(2017, 1, 1, 22, 10), "more fixing"))

# 2.) Start UI
from tkinter import *
from tkinter import ttk
from CustomWidgets import *


root = Tk()
root.title("haphi - Time Tracker")
root.minsize(width=880, height=300)
root.resizable(width=False, height=True)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

tiTable = TimeTable(root, track)
tiTable.frame.grid(column=0, row=0, sticky=(N, W, E, S))


root.mainloop()
