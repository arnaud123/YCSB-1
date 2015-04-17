__author__ = 'arnaud'

import subprocess
import time

def deleteAllElasticsearchData(ipNodeInCluster):
    exitCode = subprocess.call(['curl', '-XDELETE', 'http://' + ipNodeInCluster + ':9200/es.ycsb/'])
    if exitCode != 0:
        raise Exception("Failed to delete all data from Elasticsearch cluster")
    time.sleep(60)
