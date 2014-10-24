

class MeasurementSeries:

    def __init__(self, timepoint, measurement):
        self._timepoint = timepoint
        self._writeMeasurement = measurement
        self._readMeasurement = []

    def _getStarTimeFirstReadOperation(self):
        return self._readMeasurement[0].getStartMeasurement()

    def _getStartTimeWriteOperation(self):
        return self._writeMeasurement.getStartMeasurement()

    def add(self, measurement):
        self._readMeasurement.append(measurement)

    def getTimeToReachConsistency(self):
        for i in range(len(self._readMeasurement)-1, -1, -1):
            currentMeasurement = self._readMeasurement[i]
            if currentMeasurement.getValue() != self._timepoint:
                if i == len(self._readMeasurement)-1:
                    return None
                else:
                    return self._readMeasurement[i+1].getStartMeasurement()
        return self._readMeasurement[0].getStartMeasurement()

    def isFirstReadHappeningBeforeWrite(self):
        timeWriteOperation = self._getStartTimeWriteOperation()
        timeFirstReadOperation = self._getStarTimeFirstReadOperation()
        return timeWriteOperation > timeFirstReadOperation

    def isTimeoutViolated(self, timeoutInMicros, accurracyInMicros):
        for i in range(0, len(self._readMeasurement)):
            measurement = self._readMeasurement[i]
            startTimeMeasurement = measurement.getStartMeasurement()
            expectedStartTime = i*accurracyInMicros
            if expectedStartTime + timeoutInMicros < startTimeMeasurement:
                return True
        return False