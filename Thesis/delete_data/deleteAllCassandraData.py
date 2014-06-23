from time import sleep;
from Thesis.util.util import executeCommandOverSsh

CASSANDRA_CLI_CMD = 'cassandra-cli -f ';

def clearCassandraColumnFamily(ipsInCluster):
    for ip in ipsInCluster:
        executeCommandOverSsh(ip, 'systemctl stop cassandra; rm -rf /var/lib/cassandra/data/*; rm -rf /var/lib/cassandra/commitlog/*; rm -rf /var/lib/cassandra/saved_caches/*');
    for ip in ipsInCluster:
        executeCommandOverSsh(ip, 'systemctl start cassandra');
    sleep(10);
    cassandraCliCommands = """\"CREATE KEYSPACE usertable
with placement_strategy = 'org.apache.cassandra.locator.SimpleStrategy'
and strategy_options = [{replication_factor:3}];
use usertable;
create column family data;\""""
    executeCommandOverSsh(ipsInCluster[0], 'echo ' + cassandraCliCommands + ' > /tmp/create_columnFamily');
    sleep(20);
    executeCommandOverSsh(ipsInCluster[0], CASSANDRA_CLI_CMD + '/tmp/create_columnFamily');
    sleep(20);
