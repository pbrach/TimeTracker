from DataObjects import  *

# 1.) Create a track with example data
track = TimeTrack("TestTrack")

track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 8, 15), datetime(2016, 12, 30, 12, 30), "Planning arichtecture"))
track.addTimeSpan(TimeSpan(datetime(2016, 12, 30, 13, 00), datetime(2016, 12, 30, 18, 30), "Implementing"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 10, 00), datetime(2017, 1, 1, 16, 30), "Fixing stuff"))
track.addTimeSpan(TimeSpan(datetime(2017, 1, 1, 20, 00), datetime(2017, 1, 1, 22, 10), "more fixing"))


# 2.) Start UI
from tkinter import *
from tkinter import ttk
from CustomWidgets import *


root = Tk()
root.title("haphi - Time Tracker")
root.minsize(width=300, height=300)

tiTable = TimeTable(root, track)
tiTable.frame.grid(column=1, row=1, sticky=(N, W, E, S))


root.mainloop()
