from Thesis.consistency.processConsistencyResult.Measurement import Measurement;
from Thesis.consistency.processConsistencyResult.DataAboutConsistency import DataAboutConsistency

class FileParser(object):

    def parse(self, pathToFile, amountOfReadThreads, timeout):
        lines = self.__getLinesInFile(pathToFile);
        del lines[0];
        dataAboutConsistency = DataAboutConsistency(amountOfReadThreads);
        for line in lines:
            if not ',' in  line:
                continue;
            line = line.strip(' \n');
            splittedLine = line.split(',');
#             if(splittedLine[4] == 'null'):
#                 continue;
            timepoint = long(splittedLine[0]);
            threadId = splittedLine[1];
            startPoint = long(splittedLine[2]);
            delay = long(splittedLine[3]);
            # value = long(splittedLine[4]);
            if(delay >= timeout):
                continue;
            if(splittedLine[4] == 'null'):
                value = -1;
            else:
                value = long(splittedLine[4]);
            measurement = Measurement(startPoint, delay, value);
            dataAboutConsistency.add(timepoint, threadId, measurement);
        return dataAboutConsistency;

    def __getLinesInFile(self, pathToFile):
        f = open(pathToFile, 'r');
        linesInFile = f.readlines();
        f.close(); 
        return linesInFile;