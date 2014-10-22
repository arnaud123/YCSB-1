import subprocess;
from time import sleep;

from util.util import checkExitCodeOfProcess

class TimeToConsistencyPlot(object):

    PATH_TO_PLOT_SCRIPT = '/root/YCSB/Thesis/plot/plot_consistency_result.r';
    PATH_TO_COMBINED_PLOT_SCRIPT = '/root/YCSB/Thesis/plot/plot_combined_consistency_result.R';

    def __init__(self, dataAboutConsistency):
        self.dataAboutConsistency = dataAboutConsistency;
    
    def plotLatestConsistency(self, outputFile):
        consistencyDataFunction = self.dataAboutConsistency.getLatestTimeToConsistencyPerThread;
        self.__plot(consistencyDataFunction, outputFile);
    
    def plotEarliestConsistentcy(self, outputFile):
        consistencyDataFunction = self.dataAboutConsistency.getEarliestTimeToConsistencyPerThread;
        self.__plot(consistencyDataFunction, outputFile);
    
    def plotEarliestAndLatestConsistency(self, outputFile):
        f = open(outputFile, 'w');
        f.write(self.__getHeaderCombinedPlot() + '\n');
        for timepoint in self.dataAboutConsistency.getTimePoints():
            earliestTimeToConsistency = self.dataAboutConsistency.getEarliestTimeToConsistencyPerThread(timepoint);
            latestTimeToConsistency = self.dataAboutConsistency.getLatestTimeToConsistencyPerThread(timepoint);
            output = str(timepoint);
            output += ',' + str(self.dataAboutConsistency.getWriterThreadStartTime(timepoint));
            output += ',' + str(self.dataAboutConsistency.getWriterThreadEndTime(timepoint));
            for threadId in self.dataAboutConsistency.getReadThreadIds():
                if(threadId in earliestTimeToConsistency.keys()):
                    output += ',' + str(self.dataAboutConsistency.getReaderThreadStartTime(timepoint, threadId));
                    output += ',' + str(earliestTimeToConsistency[threadId]);
                    output += ',' + str(latestTimeToConsistency[threadId]);
                else:
                    output += ',NA,NA,NA';
            f.write(output + '\n');
        f.close(); 
        sleep(5);
        exitCode = subprocess.call(['Rscript', self.PATH_TO_COMBINED_PLOT_SCRIPT, outputFile]);
        checkExitCodeOfProcess(exitCode, 'Failed to execute plot script');

    def __getHeaderCombinedPlot(self):
        result = 'time, Wstart, Wstop';
        for threadId in self.dataAboutConsistency.getReadThreadIds():
            result += ', ' + threadId + '_start, ' + threadId + '_earliest, ' + threadId + '_latest';
        return (result);
    
    def __plot(self, retrieveConsistencyDataFunction, outputFile):
        f = open(outputFile, 'w');
        f.write(self.__getHeader() + '\n');
        for timepoint in self.dataAboutConsistency.getTimePoints():
            timeToConsistency = retrieveConsistencyDataFunction(timepoint);
            output = str(timepoint);
            output += ',' + str(self.dataAboutConsistency.getWriterThreadStartTime(timepoint));
            output += ',' + str(self.dataAboutConsistency.getWriterThreadEndTime(timepoint));
            for threadId in self.dataAboutConsistency.getReadThreadIds():
                if(threadId in timeToConsistency.keys()):
                    output += ',' + str(self.dataAboutConsistency.getReaderThreadStartTime(timepoint, threadId));
                    output += ',' + str(timeToConsistency[threadId]);
                else:
                    output += ',NA,NA';
            f.write(output + '\n');
        f.close(); 
        sleep(5);
        exitCode = subprocess.call(['Rscript', self.PATH_TO_PLOT_SCRIPT, outputFile]);
        checkExitCodeOfProcess(exitCode, 'Failed to execute plot script');
    
    def __getHeader(self):
        result = 'time, Wstart, Wstop';
        for threadId in self.dataAboutConsistency.getReadThreadIds():
            result += ', ' + threadId + '_st, ' + threadId + '_con';
        return (result);