import sys;

from Thesis.cluster.MySqlCluster import MySqlCluster;
from Thesis.load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'jdbc';
CONSISTENCY_BINDING = 'jdbc_consistency';
IPS_IN_CLUSTER = ['172.16.33.11', '172.16.33.12', '172.16.33.13'];
IP_MASTER_NODE = '172.16.33.11';
PATH_DB_PROPERTIES_FILE = '/root/YCSB/jdbc/db_properties';

def main():
    if len(sys.argv) < 5:
        printUsageAndExit();
    pathToWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    listOfAmountOfThreads = sys.argv[4].split(',');
    cluster = MySqlCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, IP_MASTER_NODE, PATH_DB_PROPERTIES_FILE);
    runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, listOfAmountOfThreads);

def printUsageAndExit():
    print 'usage: binary <path workload file> <result dir> <runtime benchmark> <list of #threads>';
    exit();

main();
