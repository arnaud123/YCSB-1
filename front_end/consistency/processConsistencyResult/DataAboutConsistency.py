from consistency.processConsistencyResult.TheadMeasurement import ThreadMeasurement;

class DataAboutConsistency(object):
    
    def __init__(self, amountOfThreads):
        # This is a dict from timepoints to ThreadMeasurements
        self.data = {};
        self.amountOfThreads = amountOfThreads;
    
    def add(self, timepoint, threadId, measurement):
        if(not timepoint in self.data.keys()):
            threadMeasurement = ThreadMeasurement(measurement);
            self.data[timepoint] = threadMeasurement;
        else:
            threadMeasurement = self.data[timepoint];
            threadMeasurement.add(threadId, measurement);
    
    def getTimePoints(self):
        return sorted(self.data.keys());
    
    def getReadThreadIds(self):
        result = [];
        for i in range(0,self.amountOfThreads):
            result.append('R-' + str(i));
        return result;
    
    def getLatestTimeToConsistencyPerThread(self, timepoint):
        threadMeasurement = self.data[timepoint];
        return threadMeasurement.getLatestTimeToConsistencyPerThread();
    
    def getEarliestTimeToConsistencyPerThread(self, timepoint):
        threadMeasurement = self.data[timepoint];
        return threadMeasurement.getEarliestTimeConsistentValuePerThread();
    
    def getAmountOfSwapsPerThread(self, timepoint):
        threadMeasurements = self.data[timepoint];
        return threadMeasurements.getAmountOfSwapsPerThread();
    
    def getReaderThreadStartTime(self, timepoint, threadId):
        threadMeasurement = self.data[timepoint];
        return threadMeasurement.getStartTimeReaderThread(threadId);
    
    def getWriterThreadStartTime(self, timepoint):
        return self.data[timepoint].getStartTimeWriterThread();
        
    def getWriterThreadEndTime(self, timepoint):
        return self.data[timepoint].getEndTimeWriterThread();
    
    # Checks the amount of inconsistencies detected by the first
    # reader thread (R-0).
    def getAmountOfInconsistentReads(self):
        amountOfInconsistentMeasures = 0;
        for timepoint in self.getTimePoints():
#             earliestTimeToConsistency = self.getEarliestTimeToConsistencyPerThread(timepoint);
#             latestTimeToConsistency = self.getLatestTimeToConsistencyPerThread(timepoint);
#             if 'R-0' in earliestTimeToConsistency and \
#                'R-0' in latestTimeToConsistency and \
#                (earliestTimeToConsistency['R-0'] < latestTimeToConsistency['R-0']):
#                 amountOfInconsistentMeasures += 1;
            amountOfInconsistentMeasures += self.data[timepoint].getAmountOfInconsistentReads('R-0');
        return amountOfInconsistentMeasures;