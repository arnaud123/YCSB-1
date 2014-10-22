import subprocess;
from time import sleep;

from util.util import checkExitCodeOfProcess

class AmountOfSwapsPlot(object):
    
    PATH_TO_PLOT_SCRIPT = '/root/YCSB/Thesis/plot/plot_amount_of_swaps.r';
    
    def __init__(self, dataAboutConsistency):
        self.dataAboutConsistency = dataAboutConsistency;
        
    def plot(self, outputFile):
        f = open(outputFile, 'w');
        f.write(self.__getHeader() + '\n');
        for timepoint in self.dataAboutConsistency.getTimePoints():
            amountOfSwapsPerThread = self.dataAboutConsistency.getAmountOfSwapsPerThread(timepoint)
            output = str(timepoint);
            for threadId in self.dataAboutConsistency.getReadThreadIds():
                if(threadId in amountOfSwapsPerThread.keys()):
                    output += ',' + str(amountOfSwapsPerThread[threadId]);
                else:
                    output += ', NA';
            f.write(output + '\n');
        f.close();
        sleep(5);
        exitCode = subprocess.call(['Rscript', self.PATH_TO_PLOT_SCRIPT, outputFile]);
        checkExitCodeOfProcess(exitCode, 'Plotting amount of swaps failed');
        
    def __getHeader(self):
        result = 'time';
        for threadId in self.dataAboutConsistency.getReadThreadIds():
            result += ', ' + threadId;
        return result;