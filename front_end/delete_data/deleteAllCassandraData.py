from time import sleep;

from util.util import executeCommandOverSsh


CASSANDRA_CLI_CMD = 'cassandra-cli -f ';

def clearCassandraKeyspace(ipsInCluster):
    ip = ipsInCluster[0]
    dropKeyspace(ip)
    sleep(10)
    createKeyspace(ip)

def dropKeyspace(accessNode):
    pathDropKeyspaceFile = "/tmp/drop_keyspace"
    executeCommandOverSsh(accessNode, 'echo "drop keyspace usertable" > ' + pathDropKeyspaceFile);
    sleep(3);
    executeCommandOverSsh(accessNode, CASSANDRA_CLI_CMD + ' ' + pathDropKeyspaceFile);

def createKeyspace(accessNode):
    pathCreateKeyspaceFile = "/tmp/create_keyspace"
    cassandraCliCommands = """\"CREATE KEYSPACE usertable
with placement_strategy = 'org.apache.cassandra.locator.SimpleStrategy'
and strategy_options = [{replication_factor:3}];
use usertable;
create column family data;\""""
    executeCommandOverSsh(accessNode, 'echo ' + cassandraCliCommands + ' > ' + pathCreateKeyspaceFile);
    sleep(3);
    executeCommandOverSsh(accessNode, CASSANDRA_CLI_CMD + ' ' + pathCreateKeyspaceFile);
