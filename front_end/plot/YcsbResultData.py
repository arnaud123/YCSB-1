class YcsbResultData:
    
    def __init__(self):
        self.possibleOperations =  ['INSERT', 'UPDATE', 'READ', 'SCAN', 'DELETE'];
        self.operationDict = {};
        self.thoughput = [];
        for operation in self.possibleOperations:
            self.operationDict[operation] = [];
    
    def add(self, operation, timepoint, latency):
        if not operation in self.possibleOperations:
            raise Exception('Illegal operation: ' + operation);
        dataTuple = (timepoint, latency);
        self.operationDict[operation].append(dataTuple);
    
    def addThroughput(self, timepoint, throughput):
        dataTuple = (timepoint, throughput);
        self.thoughput.append(dataTuple);
    
    def getTimePointLatencyMappings(self, operation):
        if not operation in self.possibleOperations:
            raise Exception('Illegal operation: ' + operation);
        return list(self.operationDict[operation]);
    
    def getPossibleOperations(self):
        return list(self.possibleOperations);
    
    def hasDataForOperation(self, operation):
        if not operation in self.possibleOperations:
            raise Exception('Illegal operation: ' + operation);
        return len(self.operationDict[operation]) != 0;
    
    def getOperationsWithData(self):
        result = [];
        for operation in self.possibleOperations:
            if self.hasDataForOperation(operation):
                result.append(operation);
        return result;
    
    def getThroughput(self):
        return list(self.thoughput);