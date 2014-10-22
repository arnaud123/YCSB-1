from load.process_result import BenchmarkResult


class AggregatedBenchmarkResult:
    
    def __init__(self, listOfFilePaths):
        self.benchmarkResults = [];
        for pathToFile in listOfFilePaths:
            benchmarkResult = BenchmarkResult(pathToFile);
            self.benchmarkResults.append(benchmarkResult);
    
    def WriteToFile(self, targetFile):
        f = open(targetFile, 'w');
        f.write('[throughput], ' + str(self.getThroughput()) + '\n');
        f.write('[READ], ' + str(self.getAggregatedLatency('hasAverageReadLatency', 'getAverageReadLatency')) + '\n');
        f.write('[INSERT], ' + str(self.getAggregatedLatency('hasAverageInsertLatency', 'getAverageInsertLatency')) + '\n');
        f.write('[UPDATE], ' + str(self.getAggregatedLatency('hasAverageUpdateLatency', 'getAverageUpdateLatency')) + '\n');
        f.write('[SCAN], ' + str(self.getAggregatedLatency('hasAverageScanLatency', 'getAverageScanLatency')) + '\n');
        f.write('[DELETE], ' + str(self.getAggregatedLatency('hasAverageDeleteLatency', 'getAverageDeleteLatency')) + '\n');
        f.close();
        
    def getThroughput(self):
        result = 0;
        for benchmarkResult in self.benchmarkResults:
            result += benchmarkResult.getThroughput();
        return result;
    
    def getAggregatedLatency(self, function):
        latency = 0;
        counter = 0;
        for benchmarkResult in self.benchmarkResults:
            if getattr(benchmarkResult, 'has' + function)():
                latency += getattr(benchmarkResult, 'get' + function)();
                counter +=1;
        if counter == 0:
            return -1;
        return latency/counter;
    
    
# def printMergedAggResultsToFile(listOfAggResults, expectedThroughput, pathResultFile):
#     f = open(pathResultFile, 'w');
#     f.write('expected_throughput, real_throughput, latency\n');
#     indexCounter = 0;
#     for aggResult in listOfAggResults:
#         latency = 0;
#         counter = 0;
#         for operation in ['AverageReadLatency', 'AverageInsertLatency', 'AverageUpdateLatency', 
#                       'AverageScanLatency', 'AverageDeleteLatency']:
#             if aggResult.getAggregatedLatency(operation) > 0:
#                 latency += aggResult.getAggregatedLatency(operation);
#                 counter += 1;
#         latency = latency/counter;
#         f.write(str(expectedThroughput[indexCounter]) + ',' + str(aggResult.getThroughput()) + ', ' + str(latency) + '\n');
#         indexCounter += 1;
#     f.close();
#     
# aggs = [];
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_400_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_600_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_800_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_1000_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_1200_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_1400_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_1600_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_1800_ops']));
# aggs.append(AggregatedBenchmarkResult(['/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_2000_ops']));
# printMergedAggResultsToFile(aggs, ['400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000'], '/home/arnaud/Desktop/load_data/cassandra/1_machines_60_threads_RESULT');