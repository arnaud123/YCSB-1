from consistency.processConsistencyResult.MeasurementSeries import MeasurementSeries

class DataAboutConsistency(object):
    
    def __init__(self):
        # Map timepoints to measurements
        self._data = {}

    def add(self, timepoint, measurement):
        if not timepoint in self._data.keys():
            self._data[timepoint] = MeasurementSeries(timepoint, measurement)
        else:
            series = self._data[timepoint]
            series.add(measurement)
            self._data[timepoint] = series

    # For every timepoint there is an entry in the list containing
    # the delay to reach consistency
    # Timepoint first consistent read after non-consistent read
    def getListTimeToReachConsistency(self):
        result = []
        for timepoint in self._data.keys():
            series = self._data[timepoint]
            timeToReachConsistency = series.getTimeToReachConsistency()
            result.append(timeToReachConsistency)
        return result

    def removeWarmUpData(self, firstSecondsToRemove):
        timepointStartOfBenchmark = sorted(self._data.keys())[0]
        print("Start of benchmark: " + str(timepointStartOfBenchmark))
        keysToRemove = []
        for timepoint in self._data.keys():
            if timepoint < timepointStartOfBenchmark + firstSecondsToRemove*(10**6):
                keysToRemove.append(timepoint)
        for key in keysToRemove:
            self._data.pop(key)
