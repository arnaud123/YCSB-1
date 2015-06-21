#!/bin/python

import subprocess;
from time import sleep;

from plot.YcsbResultData import YcsbResultData;
from util.util import checkExitCodeOfProcess
import sys;

R_FILE = "front_end/plot/plot_availability_mult.r";

# For testing purposes
def main():
    if len(sys.argv) != 2:
        print("Usage <input file>");
        exit();
    pathInputFile = sys.argv[1];
    parseAndPlot(pathInputFile);

def parseAndPlot(pathInputFile):
    ycsbResultData = parseFile(pathInputFile);
    createPlots(ycsbResultData, pathInputFile);

def createPlots(ycsbResultData, outputFileTemplate):
    paths = [];
    throughputPath = outputFileTemplate + '_THROUGHPUT_data';
    paths.append(throughputPath);
    write_data_to_plot_to_file(ycsbResultData.getThroughput(), throughputPath, 'sec', 'throughput');
    for operation in ycsbResultData.getOperationsWithData():
        outputFile = outputFileTemplate + '_' + str(operation) + '_data';
        paths.append(outputFile);
        write_data_to_plot_to_file(ycsbResultData.getTimePointLatencyMappings(operation), outputFile, 'ms', 'latency');
    sleep(5);
    command = ['Rscript', R_FILE];
    command.extend(paths);
    command.append(outputFileTemplate);
    exitCode = subprocess.call(command);
    checkExitCodeOfProcess(exitCode, 'plot script failed');
        
def write_data_to_plot_to_file(valuesMap, outputFile, firstColHeader, secondColHeader):
    f = open(outputFile, 'w');
    f.write(str(firstColHeader) + ',' + str(secondColHeader) + '\n');
    for (key,value) in valuesMap:
        f.write(str(key) + ',' + str(value) + '\n');
    f.close();

def parseFile(pathToFile):
    result = YcsbResultData();
    f = open(pathToFile, 'r');
    for line in f:
        operationId = getOperationId(line);
        if operationId != None:
            splittedLine = line.split(',');
            timePoint = splittedLine[1].strip(' \n');
            latency = splittedLine[2].strip(' \n');
            if isInteger(timePoint):
                result.add(operationId, int(timePoint), float(latency));
        elif isThroughputStatement(line):
            (timepoint, throughput) = getThroughputData(line);
            result.addThroughput(timepoint, throughput);
    f.close();
    return result;

def isInteger(s):
    try:
        int(s);
    except ValueError:
        return False;
    return True;

def isThroughputStatement(line):
    return (line.find("current ops/sec") != -1);

def getThroughputData(line):
    if not isThroughputStatement(line):
        raise Exception('Not a throughput statement');
    splittedLine = line.split(';');
    timepointPart = splittedLine[0].strip(' \n');
    throughputPart = splittedLine[1].strip(' \n');
    timepoint = timepointPart.split(' ')[0];
    throughput = throughputPart.split(' ')[0];
    return (int(timepoint), float(throughput));

def getOperationId(line):
    if line[0:1] != '[':
        return None;
    endOperationId = line.find(']');
    if endOperationId == -1:
        raise Exception('Illegal line in result file: ' + line);
    result = line [1:endOperationId];
    if result in ['CLEANUP', 'OVERALL']:
        return None;
    return result;

# main();
