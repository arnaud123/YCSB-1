import sys;

from load.loadBenchmark import runLoadBenchmarkAsBatch;
from cluster.MySqlCluster import MySqlCluster;

NORMAL_BINDING = 'jdbc';
CONSISTENCY_BINDING = 'jdbc_consistency';
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17', '172.16.8.18'];
IP_MASTER_NODE = '172.16.8.16';
PATH_DB_PROPERTIES_FILE = 'jdbc/db_properties';

def main():
    if len(sys.argv) < 7:
        printUsageAndExit(); 
    pathToWorkloadFile = sys.argv[1];
    dirToWriteResultTo = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    listOfOpsPerSec = sys.argv[4].split(',');
    listOfAmountThreads = sys.argv[5].split(',');
    listOfAmountOfMachines = sys.argv[6].split(',');
    if len(sys.argv) >= 8:
        remoteYcsbNodes = sys.argv[7].split(',');
    else:
        remoteYcsbNodes = [];
    cluster = MySqlCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, IP_MASTER_NODE, PATH_DB_PROPERTIES_FILE);
    cluster.writeDbPropertiesFile(remoteYcsbNodes);
    runLoadBenchmarkAsBatch(cluster, remoteYcsbNodes, pathToWorkloadFile, 
                        runtimeBenchmarkInMinutes, dirToWriteResultTo, 
                        listOfOpsPerSec, listOfAmountThreads, listOfAmountOfMachines);

def printUsageAndExit():
    print('usage: binary <path workload file> <result dir> <runtime benchmark> <list of #ops> <list of #threads> <list of #machines> [<list remote ycsb nodes>]');
    exit();

# cluster = MySqlCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, IP_MASTER_NODE, PATH_DB_PROPERTIES_FILE);
# remoteYcsbNodes = ['172.16.33.10'];
# cluster.writeDbPropertiesFile(remoteYcsbNodes);
# runLoadBenchmarkAsBatch(cluster, remoteYcsbNodes, '/root/YCSB/workloads/workload_load',
#                         3, '/root/YCSB/loads/mysql',
#                         ['1000000000'], ['1'], ['1']);

main();