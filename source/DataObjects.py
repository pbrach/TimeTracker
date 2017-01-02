from datetime import datetime, date, timedelta, time


def _registerNewHandler( EventHandlerList, Handler):
    if Handler not in EventHandlerList:
        EventHandlerList.append(Handler)


def _callAll(instance, callbackList):
    for func in callbackList:
        res = func(instance)


# -------------------
# TimeSpan Class
# -------------------
class TimeSpan:

    def __init__(self, start = datetime(1, 1, 1), end = datetime(1, 1, 1), description = ""):
        self.description = description

        self._start = start
        self._end = end

        self._startTime = start.time()
        self._startDate = start.date()

        self._endTime = end.time()
        self._endDate = end.date()

        self.__dateChangedHandlers = list()
        self.__timeChangedHandlers = list()


    #-------------------------------------
    # ---------------- Getter
    # -------------------------------------
    @property
    def StartTime(self):
        return self._startTime.replace()

    @property
    def EndTime(self):
        return self._endTime.replace()

    @property
    def StartDate(self):
        return self._startDate.replace()

    @property
    def EndDate(self):
        return self._endDate.replace()

    @property
    def Start(self):
        return self._start.replace()

    @property
    def End(self):
        return self._end.replace()

    @property
    def Duration(self) -> timedelta:

        tempEnd = datetime.combine(self._endDate, self._endTime)
        tempStart = datetime.combine(self._startDate, self._startTime)
        result = tempEnd - tempStart

        if result.seconds > 0:
            return result

        return timedelta()


    def contains(self, datetime):
        return  self._start <= datetime and datetime <= self._end


    def overlaps(self, otherTimeSpan):
        return  self.contains(otherTimeSpan.Start) or self.contains(otherTimeSpan.end)


    #-------------------------------------
    # ---------------- Setter
    # -------------------------------------

    def RegisterDateChangedHandler(self, handler):
        _registerNewHandler(self.__dateChangedHandlers, handler)
        return

    def RegisterTimeChangedHandler(self, handler):
        _registerNewHandler(self.__timeChangedHandlers, handler)
        return

    def SetDate(self, date : date):
        oldDate = self._startDate

        self._endDate = date
        self._startDate = date
        self._updateStart()
        self._updateEnd()

        self.FireDateChanged(self, oldDate)


    @StartTime.setter
    def StartTime(self, value : time):
        self._startTime = value
        self._updateStart()

        _callAll(self, self.__timeChangedHandlers)

    @EndTime.setter
    def EndTime(self, newTime: time):
        self._endTime = newTime
        self._updateEnd()

        _callAll(self, self.__timeChangedHandlers)


    @StartDate.setter
    def StartDate(self, newDate : date):

        oldDate = self._startDate

        self._startDate = newDate
        self._updateStart()

        self.FireDateChanged(self, oldDate)


    @EndDate.setter
    def EndDate(self, newDate: date):

        oldDate =self._endDate

        self._endDate = newDate
        self._updateEnd()

        self.FireDateChanged(self, oldDate)

    @Start.setter
    def Start(self, newTime: datetime):
        self._start = newTime
        self._startTime = newTime.time()

        oldDate = self._startDate
        self._startDate = newTime.date()

        _callAll(self, self.__timeChangedHandlers)
        self.FireDateChanged(self, oldDate)

    @End.setter
    def End(self, newTime: datetime):
        self._end = newTime
        self._endTime = newTime.time()

        oldDate = self._endDate
        self._endDate = newTime.date()

        _callAll(self, self.__timeChangedHandlers)
        self.FireDateChanged(self, oldDate)


    def _updateEnd(self):
        self._end = datetime.combine(self._endDate, self._endTime)

    def _updateStart(self):
        self._start = datetime.combine(self._startDate, self._startTime)

    def FireDateChanged(self, instance, old_date):
        for func in self.__dateChangedHandlers:
            res = func(instance, old_date)

    def unregisterAllHandler(self):
        self.__dateChangedHandlers.clear()
        self.__timeChangedHandlers.clear()

# -------------------
# TimeTrack Class
# -------------------
class TimeTrack:
    def __init__(self, name :str = "Unknown track", timeSpans : [TimeSpan] = list()):
        self.name = name
        self._timeSpans = timeSpans
        self._spanDeletedHandlers = list()


    def addTimeSpan(self, timeSpan : TimeSpan):
        self._timeSpans.append(timeSpan)

    def removeTimeSpan(self, timeSpan: TimeSpan):
        self._timeSpans.remove(timeSpan)
        self._fireSpanRemoved(timeSpan)

    def _fireSpanRemoved(self, span):
        for func in self._spanDeletedHandlers:
            res = func(span)

    def registerNewSpanDeletedHandler(self, handler):
        _registerNewHandler(self._spanDeletedHandlers, handler)


    def getTotalTime(self, fromDT : datetime = None, toDT: datetime = None) -> timedelta:

        result = timedelta()
        selectedSpans = self.getSelectedTimeSpans(fromDT, toDT)

        for span in selectedSpans:
            result += span.Duration

        return result



    def getSelectedTimeSpans(self, fromDT : datetime = None, toDT: datetime = None) -> [TimeSpan]:
        if (not fromDT is None) and (not toDT is None):
            selectedSpans = [span for span in self._timeSpans if span.startTime > fromDT and span.endTime < toDT]
        else:
            selectedSpans = self._timeSpans

        return selectedSpans



    def getSpansPerDate(self):

        spansPerDate = dict()

        for span in self._timeSpans:
            dt = span.StartDate

            if dt in spansPerDate:
                spansPerDate[dt].append(span)
                spansPerDate[dt].sort(key=lambda e: e.Start)

            else:
                spansPerDate[dt] = list()
                spansPerDate[dt].append(span)

        return spansPerDate



    def getSpansForDate(self, date):

        spanDic = self.getSpansPerDate()

        if date in spanDic:
            return spanDic[date]

        return None
