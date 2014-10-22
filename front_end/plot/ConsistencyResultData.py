class ConsistencyResultData:
    
    def __init__(self):
        self.possibleOperations = ['INSERT', 'UPDATE', 'DELETE']
        self.operationDict = {};
        for operation in self.possibleOperations:
            self.operationDict[operation] = [];
    
    def add(self, operation, time, delay):
        if not operation in self.possibleOperations:
            raise Exception('Illegal operation: ' + str(operation));
        resultTuple = (time, delay);
        self.operationDict[operation].append(resultTuple);

    def getAvarageDelayForOperation(self, operation):
        if not operation in self.possibleOperations:
            raise Exception('Illegal operation: ' + str(operation));
        averageDelay = 0;
        operationCounter = 0;
        for (_, delay) in self.operationDict[operation]:
            averageDelay += delay;
            operationCounter += 1;
        if operationCounter == 0:
            return -1;
        return averageDelay/operationCounter;
    
    def printResults(self):
        for operation in self.operationDict:
            print("=== " + operation + " ===");
            for (time, delay) in self.operationDict[operation]:
                print(str(time) + "," + str(delay));