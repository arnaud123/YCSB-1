class Measurement:
    
    def __init__(self):
        self.latencies = [];
    
    def getAverageLatency(self):
        if len(self.latencies) == 0:
            raise Exception('No latencies in Measurement'); 
        result = 0;
        for latency in self.latencies:
            result += latency;
        return result/len(self.latencies);
    
    def add(self, latency):
        self.latencies.append(latency);
        
    def hasMeasurement(self):
        return (len(self.latencies) != 0);