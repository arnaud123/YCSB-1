import operator


class MeasurementSeries:

    def __init__(self, timepoint, measurement):
        self._timepoint = timepoint
        self._writeMeasurement = measurement
        self._readMeasurement = []

    def add(self, measurement):
        self._readMeasurement.append(measurement)

    def getTimeToReachConsistency(self):
        self._readMeasurement.sort(key = operator.attrgetter('_startMeasurement'), reverse=True)
        for i in range(0, len(self._readMeasurement)):
            currentMeasurement = self._readMeasurement[i]
            if currentMeasurement.getValue() != self._timepoint:
                if i == 0:
                    raise Exception("Consistency not reached for measurement at timepoint: " + str(self._timepoint))
                else:
                    return self._readMeasurement[i-1].getStartMeasurement()
        return self._readMeasurement[-1].getStartMeasurement()