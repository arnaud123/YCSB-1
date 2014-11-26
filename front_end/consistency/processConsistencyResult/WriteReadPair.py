__author__ = 'arnaud'


class WriteReadPair(object):

    def __init__(self, writeMeasurement, readMeasurement, delayOfReadInMicros):
        self._writeMeasurement = writeMeasurement
        self._readMeasurement = readMeasurement
        self._delayOfReadInMicros = delayOfReadInMicros

    def getTimestamp(self):
        return self._writeMeasurement.getTimeStamp()

    def isValidWriteReadPair(self, timeoutInMicros):
        return not self._didReadStartBeforeWrite() and \
               self._didWriteStartBeforeTimeout(timeoutInMicros) and \
               self._didReadStartBeforeTimeout(timeoutInMicros) and \
               not self._didWriteStartTooEarly() and \
               not self._didReadStartTooEarly()

    def _didReadStartBeforeWrite(self):
        return self._writeMeasurement.getStartTimeInMicros() > self._readMeasurement.getStartTimeInMicros()

    def _didWriteStartBeforeTimeout(self, timeoutInMicros):
        return self._writeMeasurement.getStartTimeInMicros() < timeoutInMicros

    def _didReadStartBeforeTimeout(self, timeoutInMicros):
        return self._readMeasurement.getStartTimeInMicros() < self._delayOfReadInMicros + timeoutInMicros

    def _didWriteStartTooEarly(self):
        return self._writeMeasurement.getStartTimeInMicros() < 0

    def _didReadStartTooEarly(self):
        return self._readMeasurement.getStartTimeInMicros() < self._delayOfReadInMicros

    def isConsistent(self):
        return self._writeMeasurement.getValue() == self._readMeasurement.getValue()