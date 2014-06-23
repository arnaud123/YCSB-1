import subprocess;

def deleteAllDataInRiak(ipsInCluster):
    for ip in ipsInCluster:
        exitcode = subprocess.call(["ssh", "root@" + ip, "pkill -9 -u riak; su riak -c 'rm -rf /var/lib/riak/bitcask/*'"]);
        if(exitcode != 0):
            raise Exception("ssh command failed");
    for ip in ipsInCluster:
        exitcode = subprocess.call(["ssh", "root@" + ip, "su riak -c 'riak start'"]);
        if(exitcode != 0):
            raise Exception("ssh command failed");