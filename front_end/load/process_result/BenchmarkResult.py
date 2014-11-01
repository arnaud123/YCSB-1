#!/bin/python
from load.process_result.Measurement import Measurement


class BenchmarkResult:
    
    def __init__(self, pathToFile):
        self.throughput = -1;
        self.insertResults = Measurement()
        self.updateResults = Measurement();
        self.readResults = Measurement();
        self.deleteResults = Measurement();
        self.scanResults = Measurement();
        self.processFile(pathToFile);

    def processFile(self, pathToFile):
        linesOfFile = self.getLinesOfFile(pathToFile);
        for line in linesOfFile:
            self.processLine(line);

    def processLine(self, line):
        segmentId = self.getSegmentId(line);
        if segmentId is None or segmentId is 'CLEAN':
            return;
        if segmentId == 'OVERALL':
            self.processOverallSection(line);
        latency = self.getLatencyMeasurement(line);
        if latency is None:
            return;
        if segmentId == 'INSERT':
            self.insertResults.add(latency);
        if segmentId == 'UPDATE':
            self.updateResults.add(latency);
        if segmentId == 'READ':
            self.readResults.add(latency);
        if segmentId == 'SCAN':
            self.scanResults.add(latency);
        if segmentId == 'DELETE':
            self.deleteResults.add(latency);

    def getLatencyMeasurement(self, line):
        splittedLine = line.split(',');
        if len(splittedLine) != 3:
            raise Exception('Illegal measurement: ' + line);
        timepoint = splittedLine[1].strip(' \n');
        latency = splittedLine[2].strip(' \n');
        if not self.isInteger(timepoint) or int(timepoint) <= 300000:
            return None;
        return float(latency);
    
    def isInteger(self, toCheck):
        try:
            int(toCheck);
            return True;
        except ValueError:
            return False;
    
    def processOverallSection(self, line):  
        splittedLine = line.split(',');
        if len(splittedLine) != 3:
            raise Exception('Illegal throughput section: ' + line);
        if line.find('Throughput(ops/sec)') == -1:
            return; 
        if self.throughput != -1:
            raise Exception('throughput already set');
        resultPart = splittedLine[2].strip(' ');
        self.throughput = float(resultPart);
    
    def getSegmentId(self, line):
        if line[0] != '[':
            return None;
        endSegmentId = line.find(']');
        if endSegmentId == -1:
            raise Exception('Illegal segment constructionId: ' + line);
        return line[1:endSegmentId];

    def getLinesOfFile(self, pathToFile):
        f = open(pathToFile);
        lines = f.readlines();
        f.close();
        return lines;
    
    def hasThroughput(self):
        return (self.throughput != -1);
    
    def getThroughput(self):
        if not self.hasThroughput():
            raise Exception('BenchmarkResult has no throughput');
        return self.throughput;
    
    def hasAverageInsertLatency(self):
        return self.insertResults.hasMeasurement();
    
    def getAverageInsertLatency(self):
        if not self.hasAverageInsertLatency():
            raise Exception('BenchmarkResult has no average insert latency');
        return self.insertResults.getAverageLatency();
    
    
    def hasAverageUpdateLatency(self):
        return self.updateResults.hasMeasurement();    
    
    def getAverageUpdateLatency(self):
        if not self.hasAverageUpdateLatency():
            raise Exception('BenchmarkResult has no average update latency');
        return self.updateResults.getAverageLatency();
    
        
    def hasAverageReadLatency(self):
        return self.readResults.hasMeasurement();
        
    def getAverageReadLatency(self):
        if not self.hasAverageReadLatency():
            raise Exception('BenchmarkResult has no average read latency');
        return self.readResults.getAverageLatency();

    
    def hasAverageScanLatency(self):
        return self.scanResults.hasMeasurement();
        
    def getAverageScanLatency(self):
        if not self.hasAverageScanLatency():
            raise Exception('BenchmarkResult has no average scan latency');
        return self.scanResults.getAverageLatency();
    
    
    def hasAverageDeleteLatency(self):
        return self.deleteResults.hasMeasurement();
        
    def getAverageDeleteLatency(self):
        if not self.hasAverageDeleteLatency():
            raise Exception('BenchmarkResult has no average delete latency');
        return self.deleteResults.getAverageLatency();