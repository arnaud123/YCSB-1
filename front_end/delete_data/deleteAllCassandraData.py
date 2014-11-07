from time import sleep;

from util.util import executeCommandOverSsh


def clearCassandraKeyspace(ipsInCluster):
    ip = ipsInCluster[0]
    dropKeyspace(ip)
    sleep(10)
    createKeyspace(ip)
    executeCompaction(ipsInCluster)
    sleep(20)

def dropKeyspace(accessNode):
    pathDropKeyspaceFile = "/tmp/drop_keyspace"
    executeCommandOverSsh(accessNode, 'echo "DROP KEYSPACE usertable;" > ' + pathDropKeyspaceFile);
    sleep(3);
    cassandraCliCommand = getCassandraCliCommand(accessNode, pathDropKeyspaceFile)
    executeCommandOverSsh(accessNode, cassandraCliCommand);

def createKeyspace(accessNode):
    pathCreateKeyspaceFile = "/tmp/create_keyspace"
    cassandraCliCommands = """\"CREATE KEYSPACE usertable
with placement_strategy = 'org.apache.cassandra.locator.SimpleStrategy'
and strategy_options = [{replication_factor:3}];
use usertable;
create column family data;\""""
    executeCommandOverSsh(accessNode, 'echo ' + cassandraCliCommands + ' > ' + pathCreateKeyspaceFile);
    sleep(3);
    cassandraCliCommand = getCassandraCliCommand(accessNode, pathCreateKeyspaceFile)
    executeCommandOverSsh(accessNode, cassandraCliCommand);

def getCassandraCliCommand(ip, pathCommandFile):
    return "cassandra-cli -h " + ip + " -f " + pathCommandFile

def executeCompaction(ipsInCluster):
    for ip in ipsInCluster:
        command = "nodetool compact"
        executeCommandOverSsh(ip, command)