from DataObjects import TimeSpan, TimeTrack, date, datetime, time, timedelta
from tkinter import *
from tkinter import ttk


def _durationToStr(duration: timedelta):
    mm, ss = divmod(duration.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%d:%02d" % (hh, mm)
    if duration.days:
        def plural(n):
            return n, abs(n) != 1 and "s" or ""

        s = ("%d day%s, " % plural(duration.days)) + s
    return s

class ResourcesContext:

    DeleteImage = None

    def __init__(self):
        pass

    @staticmethod
    def Initialize():
        ResourcesContext.DeleteImage = PhotoImage(file="../resources/delete-16.png")



class TableRow:

    # TableRow -
    def __createRowFrame(self, root: Frame):
        frame = ttk.Frame(root, padding="2 2 2 2")
        frame.rowconfigure(0, weight=0)
        frame.grid_columnconfigure(0, weight=10)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        frame.grid_columnconfigure(4, weight=1)
        frame.grid_columnconfigure(5, weight=1)

        frame['borderwidth'] = 2
        frame['relief'] = "groove"

        return frame

    # TableRow -
    def __init__(self, root : Frame, inSpan : TimeSpan):
        self.timeSpan = inSpan
        self.frame = self.__createRowFrame(root)

        self.labels = dict()

        self.labels["DateLabel"] = ttk.Entry(self.frame, foreground="black", background="gray")
        self.labels["DateLabel"].grid(column=0, row=0, sticky=(N, W, E, S))
        self.labels["DateLabel"].configure(width="11")
        self.labels["DateLabel"].bind('<FocusOut>', self.__readDate)

        self.labels["StartLabel"] = ttk.Entry(self.frame, foreground="black", background="gray")
        self.labels["StartLabel"].grid(column=1, row=0, sticky=(N, W, E, S))
        self.labels["StartLabel"].configure(width="6")
        self.labels["StartLabel"].bind('<FocusOut>', self.__readStartTime)

        self.labels["EndLabel"] = ttk.Entry(self.frame, foreground="black", background="gray")
        self.labels["EndLabel"].grid(column=2, row=0, sticky=(N, W, E, S))
        self.labels["EndLabel"].configure(width="6")
        self.labels["EndLabel"].bind('<FocusOut>', self.__readEndTime)

        self.labels["DescriptionLabel"] = ttk.Entry(self.frame, foreground="black", background="gray")
        self.labels["DescriptionLabel"].grid(column=3, row=0, sticky=(N, W, E, S))
        self.labels["DescriptionLabel"].configure(width="70")
        self.labels["DescriptionLabel"].bind('<FocusOut>', self.__readDescription)

        self.labels["DurationLabel"] = ttk.Entry(self.frame, foreground="black", background="gray")
        self.labels["DurationLabel"].configure(width="6")
        self.labels["DurationLabel"].grid(column=4, row=0, sticky=(N, W, E, S))

        self.__initEntryText()


    # TableRow -
    def __initEntryText(self):
        self.labels["DateLabel"].insert(0, self.timeSpan.StartDate.strftime("%Y-%m-%d"))
        self.labels["StartLabel"].insert(0, self.timeSpan.StartTime.strftime("%H:%M"))
        self.labels["EndLabel"].insert(0, self.timeSpan.EndTime.strftime("%H:%M"))
        self.labels["DescriptionLabel"].insert(0, self.timeSpan.description )

        self.labels["DurationLabel"].configure(state="normal")
        self.labels["DurationLabel"].insert(0, _durationToStr(self.timeSpan.Duration) )
        self.labels["DurationLabel"].configure(state="readonly")

    # TableRow -
    def refreshView(self):
        if( len(self.frame.children) == 0):
            return

        self.labels["DurationLabel"].configure(state="normal")

        for entry in self.labels.values():
            entry.delete(0, 'end')

        self.labels["DateLabel"].insert(0, self.timeSpan.StartDate.strftime("%Y-%m-%d"))
        self.labels["StartLabel"].insert(0, self.timeSpan.StartTime.strftime("%H:%M"))
        self.labels["EndLabel"].insert(0, self.timeSpan.EndTime.strftime("%H:%M"))
        self.labels["DescriptionLabel"].insert(0, self.timeSpan.description )

        self.labels["DurationLabel"].insert(0, _durationToStr( self.timeSpan.Duration) )

        self.labels["DurationLabel"].configure(state="readonly")

    # TableRow -
    def __readDate(self, *args):

        dateString = self.labels["DateLabel"].get()
        newDate = datetime.strptime(dateString,"%Y-%m-%d").date()

        if (newDate != self.timeSpan.StartDate):
            self.timeSpan.SetDate( newDate )

            self.refreshView()

    # TableRow -
    def __readStartTime(self, *args):

        timeString = self.labels["StartLabel"].get()
        newTime = datetime.strptime(timeString,"%H:%M").time()

        if(newTime != self.timeSpan.StartTime):
            self.timeSpan.StartTime = newTime

            self.refreshView()

    # TableRow -
    def __readEndTime(self, *args):

        timeString = self.labels["EndLabel"].get()
        newTime = datetime.strptime(timeString, "%H:%M").time()

        if (newTime != self.timeSpan.EndTime):
            self.timeSpan.EndTime = newTime

            self.refreshView()

    # TableRow -
    def __readDescription(self, *args):

        descriptionText = self.labels["DescriptionLabel"].get()

        if( self.timeSpan.description != descriptionText):
            self.timeSpan.description = descriptionText

            self.refreshView()




class RowContainer:

    # RowContainer - destroy
    def destroyContainer(self):
        self.frame.destroy()

        for tr in self.tableRows:
            tr.timeSpan.unregisterAllHandler()


    # RowContainer - __init__
    def  __init__(self, root : Frame, date, spans, track):
        self.rowIdx = 0
        self.frame = ttk.Frame(root, padding="2 2 2 2")
        self.frame['borderwidth'] = 2
        self.frame['relief'] = "groove"

        self.date = date
        self.track = track
        self.spans = spans
        self.totalTimeText = StringVar()

        self.tableRows = list()
        self.totalDurationLabel = None
        self.dateLabel = None

        self._createDateContainer()
        self._rowIdx = -1


    # RowContainer - RowIndex
    @property
    def RowIndex(self):
        return self.rowIdx

    # RowContainer - RowIndex
    @RowIndex.setter
    def RowIndex(self, newIndex : int):
        self._rowIdx = newIndex

        self.frame.grid(column=0, row=self._rowIdx, sticky=(N, W, E, S))


    # RowContainer - _createDateContainer
    def _createDateContainer(self):

        # 1.) Setup the label row for the container
        labelText = self.date.strftime("%Y-%m-%d (%a)")
        self.dateLabel = ttk.Label(self.frame, text=labelText, foreground="black", background="gray", justify="left")
        self.dateLabel.grid(column=0, row=self.rowIdx, sticky=(E,W) )

        # 2.) Create a total hours row
        self.totalTimeText.set( "Total: " + _durationToStr( self._getTotalDuration() ) )
        self.totalDurationLabel = ttk.Label(self.frame, textvariable=self.totalTimeText, foreground="black", background="gray", justify="right")
        self.totalDurationLabel.grid( column=1, columnspan=2, row=self.rowIdx, sticky=(E,W) )

        self.rowIdx += 1

        # 3.) Create rows for every span
        for span in self.spans:
            span.RegisterTimeChangedHandler(self._updateTotalTime)

            tr = TableRow(self.frame, span)
            tr.frame.grid(column=0, columnspan=2, row=self.rowIdx)

            def deleteAction(*args):
                self.track.removeTimeSpan(span)

            deleteButton = ttk.Button(self.frame, image=ResourcesContext.DeleteImage, command=deleteAction)
            deleteButton.grid(column=2, row=self.rowIdx)

            self.tableRows.append(tr)
            self.rowIdx += 1


    def _updateTotalTime(self, span):
        self.totalTimeText.set("Total: " + _durationToStr(self._getTotalDuration()))

    # RowContainer - _getTotalDuration
    def _getTotalDuration(self):
        totalOfDay = timedelta()

        for span in self.spans:
            totalOfDay += span.Duration

        return totalOfDay






class TimeTable:
    # TimeTable - __init__
    def  __init__(self, root : Frame, in_track: TimeTrack):
        ResourcesContext.Initialize()
        self.rowIdx = 0
        self.dateContainers = dict()

        self.frame = ttk.Frame(root, padding="2 2 2 2")
        self.frame['borderwidth'] = 2
        self.frame['relief'] = "groove"

        self.track = in_track
        self.track.registerNewSpanDeletedHandler( self._hanleSpanRemoved)

        self.header = self.__createRowHeader(self.frame, "Date", "Start", "End", "Description", "Hours")
        self.header.grid(column=0, row=self.rowIdx, sticky=(N, W, E, S))
        self.rowIdx += 1

        self._createContainer()

        self._createFooter()



    # TimeTable - _createDateRows
    def _createContainer(self):

        for date, spans in self.track.getSpansPerDate().items():

            self.dateContainers[date] = RowContainer(self.frame, date, spans, self.track)

            self.dateContainers[date].RowIndex = self.rowIdx
            self.rowIdx += 1

            for span in spans:
                span.RegisterDateChangedHandler( self._handleDateChanged)


    # TimeTable - _handleDateChanged
    def _handleDateChanged(self, timeSpan : TimeSpan, oldDate : date):
        # 0.) Sanity check: nothing to do if the dates actually did not change
        newDate = timeSpan.StartDate
        if newDate == oldDate:
            return

        # 1.) refresh the view
        self.refreshView()

    def _hanleSpanRemoved(self, span):
        # 1.) refresh the view
        self.refreshView()

    def refreshView(self):
        # 1.) destroy all
        for container in self.dateContainers.values():
            container.destroyContainer()

        self.dateContainers.clear()

        # 2.) ReDraw all
        self._createContainer()
        self._correctRowIndices()



    # TimeTable - _correctRowIndices
    def _correctRowIndices(self):
        sortedDates = sorted(self.dateContainers.keys())

        for (idx, date) in zip(range(1, len(sortedDates)+1 ), sortedDates):
            self.dateContainers[date].RowIndex = idx

        self.footer.grid(column=0, row=len(sortedDates)+1, sticky=(N, W, E, S))


    # TimeTable - __createRowHeader
    def __createRowHeader(self, root : Frame, *lblTexts):

        frame = self.__createRowFrame(root)

        ttk.Label(frame, text=lblTexts[0], foreground="black", background="gray").grid(column=0, row=0, sticky=(N, W, E, S))
        ttk.Label(frame, text=lblTexts[1], foreground="black", background="gray").grid(column=1, row=0, sticky=(N, W, E, S))
        ttk.Label(frame, text=lblTexts[2], foreground="black", background="gray").grid(column=2, row=0, sticky=(N, W, E, S))
        ttk.Label(frame, text=lblTexts[3], foreground="black", background="gray").grid(column=3, row=0, sticky=(N, W, E, S))
        ttk.Label(frame, text=lblTexts[4], foreground="black", background="gray").grid(column=4, row=0, sticky=(N, W, E, S))

        return frame


    # TimeTable - __createRowFrame
    def __createRowFrame(self, root : Frame):

        frame = ttk.Frame(root, padding="2 2 2 2")
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=20)
        frame.columnconfigure(4, weight=1)

        frame['borderwidth'] = 6
        frame['relief'] = "groove"

        return frame

    def _createFooter(self):
        self.footer = self.__createRowFrame(self.frame)

        label = ttk.Label(self.footer, text="add new", foreground="black", background="gray")
        label.grid(column=0, row=0, sticky=( W))

        self.footer.grid(column=0, row=self.rowIdx, sticky=(N, W, E, S))
        self.rowIdx += 1

        self.footer.bind('<ButtonPress-1>', self.__addEmptyRow)
        label.bind('<ButtonPress-1>', self.__addEmptyRow)


    def __addEmptyRow(self, *args):

        newDate = datetime.combine( datetime.today().date(), time() )
        newSpan = TimeSpan(newDate, newDate)

        self.track.addTimeSpan(newSpan)

        self.refreshView()


    def getMostRecentDate(self):
        sortedDates = sorted(self.dateContainers.keys())

        return sortedDates[-1]





