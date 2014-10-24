import operator


class MeasurementSeries:

    def __init__(self, timepoint, measurement):
        self._timepoint = timepoint
        self._writeMeasurement = measurement
        self._readMeasurement = []

    def _getStarTimeFirstReadOperation(self):
        self._readMeasurement.sort(key = operator.attrgetter('_startMeasurement'), reverse=True)
        return self._readMeasurement[-1].getStartMeasurement()

    def _getStartTimeWriteOperation(self):
        return self._writeMeasurement.getStartMeasurement()

    def _getStartTimeFirstReadAfterWrite(self):
        startTimeWrite = self._writeMeasurement.getStartMeasurement()
        self._readMeasurement.sort(key = operator.attrgetter('_startMeasurement'))
        for measurement in self._readMeasurement:
            startTimeReadMeasurement = measurement.getStartMeasurement()
            if startTimeReadMeasurement > startTimeWrite:
                return startTimeReadMeasurement
        return None

    def add(self, measurement):
        self._readMeasurement.append(measurement)

    def getTimeToReachConsistency(self):
        self._readMeasurement.sort(key = operator.attrgetter('_startMeasurement'), reverse=True)
        for i in range(0, len(self._readMeasurement)):
            currentMeasurement = self._readMeasurement[i]
            if currentMeasurement.getValue() != self._timepoint:
                if i == 0:
                    return None
                else:
                    return self._readMeasurement[i-1].getStartMeasurement()
        return self._readMeasurement[-1].getStartMeasurement()

    def isTimeBetweenWriteAndFirstReadAfterWriteLessThan(self, nanos):
        timeWriteOperation = self._getStartTimeWriteOperation()
        timeFirstReadAfterWrite = self._getStartTimeFirstReadAfterWrite()
        if timeFirstReadAfterWrite is None:
            return False
        return  timeWriteOperation + nanos > timeFirstReadAfterWrite