#!/bin/python

import sys;

from plot.ConsistencyResultData import ConsistencyResultData;


def main():
    if len(sys.argv) < 2:
        printUsageAndExit();
    pathResultFile = sys.argv[1];
    f = open(pathResultFile, 'r');
    resultFileData = processFile(f);
    f.close();
    resultFileData.printResults();
    print('average insert delay: ' + str(resultFileData.getAvarageDelayForOperation('INSERT')));
    print('average update delay: ' + str(resultFileData.getAvarageDelayForOperation('UPDATE')));
    print('average delete delay: ' + str(resultFileData.getAvarageDelayForOperation('DELETE')));

def processFile(f):
    resultFileData = ConsistencyResultData()
    for line in f:
        splittedLine = line.split(',');
        if len(splittedLine) != 3:
            raise Exception('Illegal line in result file');
        operation = splittedLine[0].strip(' \n');
        time = splittedLine[1].strip(' \n');
        delay = splittedLine[2].strip(' \n');
        if not operation in ['INSERT', 'UPDATE', 'DELETE']:
            raise Exception('Illegal operation in result file: ' + operation);
        resultFileData.add(operation, int(time), float(delay));
    return resultFileData;

def printUsageAndExit():
    print('Usage: binary <path consistency result file>');
    exit(1);
    
main();