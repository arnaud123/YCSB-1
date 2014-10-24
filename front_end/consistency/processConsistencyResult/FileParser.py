from consistency.processConsistencyResult.DataAboutConsistency import DataAboutConsistency
from consistency.processConsistencyResult.Measurement import Measurement


class FileParser(object):

    def parse(self, pathToFile):
        f = open(pathToFile, 'r')
        headerLine = True
        dataAboutConsistency = DataAboutConsistency()
        for line in f:
            if headerLine:
                headerLine = False
            elif ',' in line:
                (timepoint, measurement) = self._parseLine(line)
                dataAboutConsistency.add(timepoint, measurement)
        f.close()
        return dataAboutConsistency

    def _parseLine(self, line):
        line = line.strip(' \n')
        splittedLine = line.split(',')
        timepoint = int(splittedLine[0])
        # threadId = splittedLine[1]
        startPoint = int(splittedLine[2])
        delay = int(splittedLine[3])
        if splittedLine[4] == 'null':
            value = -1
        else:
            value = int(splittedLine[4])
        return timepoint, Measurement(startPoint, delay, value)