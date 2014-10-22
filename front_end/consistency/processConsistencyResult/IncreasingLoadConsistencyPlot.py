import subprocess;

from consistency.processConsistencyResult.FileParser import FileParser;

class IncreasingLoadConsistencyPlot(object):
    
    PATH_TO_PLOT_SCRIPT = '/root/YCSB/Thesis/plot/increasing_load_consistency.R';
    
    def __init__(self, targetThroughputs, amountOfReadThreads, timeout):
        self.__targetThroughput = targetThroughputs;
        self.__amountOfReadThreads = amountOfReadThreads;
        self.__timeout = timeout;
    
    def plot(self, dataFilesInsertOperations, dataFilesUpdateOperations, outputFileTemplate):
        pathPlotDataInsertOps = outputFileTemplate + '_insert_result';
        pathPlotDataUpdateOps = outputFileTemplate + '_update_result';
        self.__writePlotDataToFile(dataFilesInsertOperations, pathPlotDataInsertOps);
        self.__writePlotDataToFile(dataFilesUpdateOperations, pathPlotDataUpdateOps);
        subprocess.call(['Rscript', self.PATH_TO_PLOT_SCRIPT, pathPlotDataInsertOps,  
                         pathPlotDataUpdateOps, outputFileTemplate + '_plot.png']);
        
    def __writePlotDataToFile(self, dataFiles, outputFile):
        f = open(outputFile, 'w');
        f.write('throughput, amountInconsistentReads\n');
        fileParser = FileParser();
        for i in range(0, len(self.__targetThroughput)):
            targetThroughput = self.__targetThroughput[i];
            dataFile = dataFiles[i];
            dataAboutConsistency = fileParser.parse(dataFile, self.__amountOfReadThreads, self.__timeout);
            amountOfInconsistentReads = dataAboutConsistency.getAmountOfInconsistentReads();
            f.write(str(targetThroughput) + ',' + str(amountOfInconsistentReads) + '\n');
        f.close();