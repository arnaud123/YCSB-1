class Measurement(object):
    
    def __init__(self, startMeasurement, endMeasurement, value):
        self.startMeasurement = startMeasurement;
        self.endMeasurement = endMeasurement;
        self.value = value;
        
    def getStartMeasurement(self):
        return self.startMeasurement;

    def getEndMeasurement(self):
        return self.endMeasurement;

    def getValue(self):
        return self.value;
    
    def isSwap(self, otherMeasurement):
        return (self.value != otherMeasurement.getValue());

    def object_compare(self, otherMeasurement):
        if(otherMeasurement is None):
            raise Exception("Parameter otherMeasurement is null");
        if(self.startMeasurement < otherMeasurement.getStartMeasurement()):
            return -1;
        if(self.startMeasurement > otherMeasurement.getStartMeasurement()):
            return 1;
        return 0;