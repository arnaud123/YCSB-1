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
        for key in self._delayAfterWriteToWriteReadMeasurementMap:
            writeReadPairs = self._delayAfterWriteToWriteReadMeasurementMap[key]
            newWriteReadPairs = self._removeWriteReadPairsInWarmupPhase(writeReadPairs, warmUpInMicros)
            newWriteReadPairs = self._removeWriteReadsPairWithTimeout(newWriteReadPairs, timeoutInMicros)
            self._delayAfterWriteToWriteReadMeasurementMap[key] = newWriteReadPairs

    def _removeWriteReadsPairWithTimeout(self, writeReadPairs, timeoutInMicros):
        result = []
        for pair in writeReadPairs:
            if pair.isValidWriteReadPair(timeoutInMicros):
                result.append(pair)
        return result

    def _removeWriteReadPairsInWarmupPhase(self, writeReadPairs, warmUpInMicros):
        smallestTimestamp = self._getSmallestTimestamp(writeReadPairs)
        indicesToRemove = []
        for i in range(len(writeReadPairs)):
            pair = writeReadPairs[i]
            if pair.getTimestamp() < smallestTimestamp + warmUpInMicros:
                indicesToRemove.append(i)
        for i in indicesToRemove:
            writeReadPairs.pop(i)
        return writeReadPairs

    def _getSmallestTimestamp(self, writeReadPairs):
        smallestTimestamp = writeReadPairs[0].getTimestamp()
        for pair in writeReadPairs:
            if pair.getTimestamp() < smallestTimestamp:
                smallestTimestamp = pair.getTimestamp()
        return smallestTimestamp

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