class ThreadMeasurement(object):
    
    def __init__(self, measurement):
        # This is a dict of a list of measurements
        self.dataForThread = {};
        self.measurementWriterThread = measurement;
    
    def add(self, threadId, measurement):
        # Only add measurements after the write threads has finished
        if(measurement.getStartMeasurement() < self.measurementWriterThread.getEndMeasurement()):
            return;
        if(not threadId in self.dataForThread.keys()):
            measurementsForThreadId = [measurement];
            self.dataForThread[threadId] = measurementsForThreadId;
        else:
            measurementsForThreadId = self.dataForThread[threadId];
            measurementsForThreadId.append(measurement);
    
    def getLatestTimeToConsistency(self):
        latestTimeToConsistency = 0;
        for threadId in self.dataForThread.keys():
            # TODO: Latest vs first
            currentLastTimeToConsistency = self.__getThreadsLatestTimeToConsistency(threadId);
            latestTimeToConsistency = max(latestTimeToConsistency, currentLastTimeToConsistency);
        return latestTimeToConsistency;
    
    def getLatestTimeToConsistencyPerThread(self):
        result = {};
        for threadId in self.dataForThread.keys():
            timeToConsistency = self.__getThreadsLatestTimeToConsistency(threadId);
            result[threadId] = timeToConsistency;
        return result;
    
    def __getThreadsLatestTimeToConsistency(self, threadId):
        result = 0;
        previousConsistent = False;
        for currentMeasurement in self.__getMeasurementsSorted(threadId):
            # TODO: Latest vs first
            if(self.__isConsistent(currentMeasurement) and not previousConsistent and currentMeasurement.getEndMeasurement() > result):
                result = currentMeasurement.getEndMeasurement();
                previousConsistent = True;
            elif(not self.__isConsistent(currentMeasurement)):
                previousConsistent = False;
        return result;
    
    def getEarliestTimeConsistentValuePerThread(self):
        result = {};
        for threadId in self.dataForThread.keys():
            timepointFirstConsistentValue = self.__getEarliestTimeConsistentValue(threadId);
            if(not timepointFirstConsistentValue is None):
                result[threadId] = timepointFirstConsistentValue;
        return result;
    
    def __getEarliestTimeConsistentValue(self, threadId):
        for currentMeasurement in self.__getMeasurementsSorted(threadId):
            if(self.__isConsistent(currentMeasurement)):
                # End or start of measurement
                return currentMeasurement.getEndMeasurement();
        return None;
    
    def __isConsistent(self, measurement):
        return (measurement.getValue() == self.getValueWriterThread());
    
    def getMostAmountOfSwapsToConsistency(self):
        currentMostAmountOfSwaps = 0;
        for threadId in self.dataForThread.keys():
            mostAmountOfSwaps = self.__getAmountOfSwaps(threadId);
            currentMostAmountOfSwaps = max(currentMostAmountOfSwaps, mostAmountOfSwaps);
        return currentMostAmountOfSwaps;
     
    def getAmountOfSwapsPerThread(self):
        result = {};
        for threadId in self.dataForThread.keys():
            amountOfSwaps = self.__getAmountOfSwaps(threadId);
            result[threadId] = amountOfSwaps;
        return result;
    
    def __getAmountOfSwaps(self, threadId):
        aConsistentValueRead = False;
        previousValueWasConsistent = False;
        swapCounter = 0;
        for measurement in self.__getMeasurementsSorted(threadId):
            if(not self.__isConsistent(measurement) and not aConsistentValueRead):
                continue;
            if(self.__isConsistent(measurement) and not aConsistentValueRead):
                aConsistentValueRead = True;
                previousValueWasConsistent = True;
            elif(self.__isConsistent(measurement) and aConsistentValueRead and not previousValueWasConsistent):
                swapCounter += 1;
                previousValueWasConsistent = True;
            elif(not self.__isConsistent(measurement) and aConsistentValueRead and previousValueWasConsistent):
                previousValueWasConsistent = False;
        return swapCounter;
    
    def getStartTimeWriterThread(self):
        return self.measurementWriterThread.getStartMeasurement();
    
    def getEndTimeWriterThread(self):
        return self.measurementWriterThread.getEndMeasurement();
    
    def getValueWriterThread(self):
        return self.measurementWriterThread.getValue();
    
    def getStartTimeReaderThread(self, threadId):
        return self.__getMeasurementsSorted(threadId)[0].getStartMeasurement();
    
    def __getMeasurementsSorted(self, threadId):
        return sorted(self.dataForThread[threadId], key=lambda measurement: measurement.getStartMeasurement());
    
    def getAmountOfInconsistentReads(self, threadId):
        if(not threadId in self.dataForThread):
            return 0;
        for measurement in self.__getMeasurementsSorted(threadId):
            # Neglect inconsistent reads by interleaving threads
            if(not self.__isConsistent(measurement) and measurement.getValue() <= self.measurementWriterThread.getValue()):
                return 1;
        return 0;