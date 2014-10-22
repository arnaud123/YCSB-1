# import subprocess;

def writeLoadDataToCsv(listInputFiles, outputFile):
    f = open(outputFile, 'w');
    f.write('throughput, latency, threads\n');
    for currentFileName in listInputFiles:
        linesOfFile = getLinesOfFile(currentFileName);
        throughput = extractRealThroughput(linesOfFile);
        latency = extractAverageLatency(linesOfFile); 
        amountOfThreads = extractAmountOfThreads(linesOfFile);
        f.write(str(throughput) + ', ' + str(latency) + ', ' + str(amountOfThreads) + ' threads\n');
    f.close();

def extractRealThroughput(lines):
    for line in lines:
        if '[OVERALL], Throughput(ops/sec)' in line:
            splittedLine = line.split(',');
            return float(splittedLine[2].strip(' \n'));
    raise Exception('Real throughput not found in file');
    
# def extractExpectedThroughput(lines):
#     amountOfThread = extractAmountOfThreads(lines);
#     averageLatency = extractAverageLatency(lines);
#     return amountOfThread*(1000000/averageLatency);
#         
# def extractAmountOfThreads(lines):
#     for line in lines:
#         index = line.find('-threads');
#         if index != -1:
#             subLine = line[index:];
#             return int(subLine.split(' ')[1].strip(' \n'));
#     raise Exception('Amount of thread not found in file');
    
def extractAverageLatency(lines):
    for line in lines:
        if '[UPDATE], AverageLatency(us)' in line:
            splittedLine = line.split(',');
            return float(splittedLine[2].strip(' \n'));
    raise Exception('Average latency not found in file');

def extractAmountOfThreads(lines):
    lineWithAmountOfThreads = lines[1];
    splittedLine = lineWithAmountOfThreads.split(' ');
    for i in range(0,len(splittedLine)):
        if '-threads' in splittedLine[i]:
            return int(splittedLine[i+1].strip(' \n'));
    raise Exception('Amount of Threads not found in file'); 

def getLinesOfFile(fileName):
    f = open(fileName, 'r');
    lines = f.readlines();
    f.close();
    return lines;


# inputFiles = ['/tmp/cassandra_10',
#             '/tmp/cassandra_20',
#             '/tmp/cassandra_30',
#             '/tmp/cassandra_40',
#             '/tmp/cassandra_50',
#             '/tmp/cassandra_60',
#             '/tmp/cassandra_70',
#             '/tmp/cassandra_80',
#             '/tmp/cassandra_90',
#             '/tmp/cassandra_100'];
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_110_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_120_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_130_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_140_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_150_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_160_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_170_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_180_threads_1000000_ops',
#             '/home/arnaud/Desktop/new_scan_load/riak/1_machines_190_threads_1000000_ops',
#              '/home/arnaud/Desktop/new_scan_load/riak/1_machines_200_threads_1000000_ops'];
# outputFile = '/tmp/cassandra_result';
#   
# writeLoadDataToCsv(inputFiles, outputFile);
# subprocess.call(['Rscript', '/home/arnaud/eclipse/workspace/Thesis/Thesis/plot/plot_load_rough_scan.r', outputFile, outputFile+'_graph.png']);