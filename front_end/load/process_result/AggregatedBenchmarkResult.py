from load.process_result.BenchmarkResult import BenchmarkResult


class AggregatedBenchmarkResult:
    
    def __init__(self, listOfFilePaths):
        self.benchmarkResults = [];
        for pathToFile in listOfFilePaths:
            benchmarkResult = BenchmarkResult(pathToFile);
            self.benchmarkResults.append(benchmarkResult);
    
    def WriteToFile(self, targetFile):
        f = open(targetFile, 'w');
        f.write('[throughput], ' + str(self.getThroughput()) + '\n');
        f.write('[READ], ' + str(self.getAggregatedLatency('hasAverageReadLatency')) + '\n');
        f.write('[INSERT], ' + str(self.getAggregatedLatency('hasAverageInsertLatency')) + '\n');
        f.write('[UPDATE], ' + str(self.getAggregatedLatency('hasAverageUpdateLatency')) + '\n');
        f.write('[SCAN], ' + str(self.getAggregatedLatency('hasAverageScanLatency')) + '\n');
        f.write('[DELETE], ' + str(self.getAggregatedLatency('hasAverageDeleteLatency')) + '\n');
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

# aggs = [];
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_1_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_5_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_10_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_15_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_20_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_50_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_100_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_150_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_200_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_250_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_300_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_350_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_400_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_450_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_500_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_550_ops']));
# aggs.append(AggregatedBenchmarkResult(['/tmp/test/1_machines_120_threads_600_ops']));
# printMergedAggResultsToFile(aggs, ['1', '5', '10', '15', '20', '50', '100', '150', '200', '250', '300', '350', '400', '450', '500', '550', '600'], '/tmp/test/RESULT');