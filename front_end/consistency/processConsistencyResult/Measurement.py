class Measurement(object):
    
    def __init__(self, timeStamp, startTimeInMicros, endTimeInMicros, value):
        self._timeStamp = timeStamp
        self._startTimeInMicros = startTimeInMicros
        self._endTimeInMicros = endTimeInMicros
        self._value = value
        
    def getTimeStamp(self):
        return self._timeStamp

    def getStartTimeInMicros(self):
        return self._startTimeInMicros

    def getEndTimeInMicros(self):
        return self._endTimeInMicros

    def getValue(self):
        return self._value