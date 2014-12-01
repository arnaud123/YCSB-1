from consistency.processConsistencyResult.ConsistencyDataset import ConsistencyDataset
from consistency.processConsistencyResult.Measurement import Measurement

class FileParser(object):

    def parse(self, delayToWriteInMicrosToFilePathPairs):
        consistencyDatset = ConsistencyDataset()
        for (delayToWriteInMicros,filePath) in delayToWriteInMicrosToFilePathPairs:
            consistencyDatset = self._parseFile(filePath, delayToWriteInMicros, consistencyDatset)
        return consistencyDatset

    def _parseFile(self, pathToFile, delayToWriteInMicros, consistencyDataset):
        f = open(pathToFile, 'r')
        f.readline()  # Remove header
        writeMeasurementLine = f.readline()
        readMeasurementLine = f.readline()
        while ',' in writeMeasurementLine and ',' in readMeasurementLine:
            consistencyDataset = self._parseWriteAndReadMeasurementLine(writeMeasurementLine, readMeasurementLine,
                                                                        consistencyDataset, delayToWriteInMicros)
            if consistencyDataset is None:
                break
            writeMeasurementLine = f.readline()
            readMeasurementLine = f.readline()
        f.close()
        return consistencyDataset

    def _parseWriteAndReadMeasurementLine(self,writeMeasurementLine, readMeasurementLine,
                                          consistencyDataset, delayToWriteInMicros):
        operationTypeWrite, writeMeasurement = self._parseLine(writeMeasurementLine)
        operationTypeRead, readMeasurement = self._parseLine(readMeasurementLine)
        if operationTypeWrite == "W-0" and operationTypeRead == "R-0":
            consistencyDataset.add(writeMeasurement, readMeasurement, delayToWriteInMicros)
        return consistencyDataset

    def _parseLine(self, line):
        line = line.strip(' \n')
        splittedLine = line.split(',')
        timeStamp = int(splittedLine[0])
        operationType = splittedLine[1]
        startTimeInMicros = int(splittedLine[2])
        endTimeInMicros = int(splittedLine[3])
        if splittedLine[4] == 'null':
            value = -1
        else:
            value = int(splittedLine[4])
        return operationType, Measurement(timeStamp, startTimeInMicros, endTimeInMicros, value)
