from BenchmarkResult import BenchmarkResult;

# import os;
# for fn in os.listdir('.'): 
#     print fn;
#     result = BenchmarkResult(fn);
#     print 'throughput: ' + str(result.getThroughput());
#     print 'hasAverageReadLatency: ' + str(result.hasAverageReadLatency());
#     print 'getAverageReadLatency: ' + str(result.getAverageReadLatency());
#     print 'hasAverageUpdateLatency: ' + str(result.hasAverageUpdateLatency());
#     print 'getAverageUpdateLatency: ' + str(result.getAverageUpdateLatency());
#     print 'hasAverageInsertLatency: ' +  str(result.hasAverageInsertLatency());
#     print 'getAverageInsertLatency: ' + str(result.getAverageInsertLatency());
#     print 'NOT PRESENT';
#     print 'hasAverageScanLatency: ' + str(result.hasAverageScanLatency());
#     print 'hasAverageDeleteLatency: ' +  str(result.hasAverageDeleteLatency());
#     print '#####################################################################';

# from AggregatedBenchmarkResult import AggregatedBenchmarkResult;
# 
# res = AggregatedBenchmarkResult(['/home/arnaud/Desktop/couchdb_data/1_machines_500_thread_25', 
#                                  '/home/arnaud/Desktop/couchdb_data/1_machines_500_thread_50',
#                                  '/home/arnaud/Desktop/couchdb_data/1_machines_500_thread_100',
#                                  '/home/arnaud/Desktop/couchdb_data/1_machines_500_thread_150',
#                                  '/home/arnaud/Desktop/couchdb_data/1_machines_500_thread_1000000']);
# res.WriteToFile('/home/arnaud/Desktop/result5.txt')


from Thesis.load.process_result.AggregatedBenchmarkResult import AggregatedBenchmarkResult;
from Thesis.load.run_loads import printMergedAggResultsToFile;
files = [];
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_5_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_6_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_7_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_8_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_9_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_10_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_11_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_12_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_13_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_14_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_15_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_16_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_17_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_18_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_19_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_20_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_21_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_22_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_23_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_24_ops');
files.append('/home/arnaud/Desktop/riak/75/1_machines_75_threads_25_ops');
results = [];
for f in files:
    res = AggregatedBenchmarkResult([f]);
    results.append(res);
printMergedAggResultsToFile(results, '/home/arnaud/Desktop/res');
    
    