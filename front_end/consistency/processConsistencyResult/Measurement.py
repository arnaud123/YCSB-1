class Measurement(object):
    
    def __init__(self, startMeasurement, endMeasurement, value):
        self._startMeasurement = startMeasurement
        self._endMeasurement = endMeasurement
        self._value = value
        
    def getStartMeasurement(self):
        return self._startMeasurement

    def getEndMeasurement(self):
        return self._endMeasurement

    def getValue(self):
        return self._value