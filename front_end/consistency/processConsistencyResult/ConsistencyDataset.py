from consistency.processConsistencyResult.WriteReadPair import WriteReadPair

__author__ = 'arnaud'

class ConsistencyDataset(object):

    def __init__(self):
        # Map time after write to their readWriteValues
        self._delayAfterWriteToWriteReadMeasurementMap = {}

    def add(self, writeMeasurement, readMeasurement, delayReadInMicros):
        writeReadPair = WriteReadPair(writeMeasurement, readMeasurement, delayReadInMicros)
        if not delayReadInMicros in self._delayAfterWriteToWriteReadMeasurementMap:
            self._delayAfterWriteToWriteReadMeasurementMap[delayReadInMicros] = [writeReadPair]
        else:
            self._delayAfterWriteToWriteReadMeasurementMap[delayReadInMicros].append(writeReadPair)

    # Consider invalue if read or read happens after timeout period
    def filterIllegalMeasurements(self, warmUpInMicros, timeoutInMicros):
        self._removeWriteReadPairsInWarmupPhase(warmUpInMicros)
        for key in self._delayAfterWriteToWriteReadMeasurementMap:
            writeReadPairs = self._delayAfterWriteToWriteReadMeasurementMap[key]
            newWriteReadPairs = self._removeWriteReadsPairWithTimeout(writeReadPairs, timeoutInMicros)
            self._delayAfterWriteToWriteReadMeasurementMap[key] = newWriteReadPairs

    def _removeWriteReadsPairWithTimeout(self, writeReadPairs, timeoutInMicros):
        result = []
        for pair in writeReadPairs:
            if pair.isValidWriteReadPair(timeoutInMicros):
                result.append(pair)
        return result

    def _removeWriteReadPairsInWarmupPhase(self, warmUpInMicros):
        smallestTimestamp = self._getSmallestTimestamp()
        keysToRemove = []
        for key in self._delayAfterWriteToWriteReadMeasurementMap:
            if key < smallestTimestamp + warmUpInMicros:
                keysToRemove.append(key)
        for key in keysToRemove:
            del self._delayAfterWriteToWriteReadMeasurementMap[key]

    def _getSmallestTimestamp(self):
        return min(self._delayAfterWriteToWriteReadMeasurementMap.keys())

    def getPercentageOfConsistentValuesPerDelayAfterWrite(self):
        result = {}
        for delayAfterWrite in self._delayAfterWriteToWriteReadMeasurementMap:
            writeReadPairs = self._delayAfterWriteToWriteReadMeasurementMap[delayAfterWrite]
            percentageOfConsistentValues = self._getPercentageOfConsistentValues(writeReadPairs)
            result[delayAfterWrite] = percentageOfConsistentValues
        return result

    def _getPercentageOfConsistentValues(self, writeReadPairs):
        counterConsistentValues = 0
        counterTotalValues = 0
        for pair in writeReadPairs:
            if pair.isConsistent():
                counterConsistentValues += 1
            counterTotalValues +=1
        return counterConsistentValues/counterTotalValues

    def getAmountOfMeasurements(self, delayAfterWriteInMicros):
        return len(self._delayAfterWriteToWriteReadMeasurementMap[delayAfterWriteInMicros])