import subprocess
import time

def deleteAllDataInMongoDb(ipAccessNode, ipDataNodes, databaseName, collectionName):
    deleteAllDataInCollection(ipAccessNode, databaseName, collectionName)
    time.sleep(10)
    freeUpUnusedSpace(ipDataNodes, databaseName)
    time.sleep(10)

def deleteAllDataInCollection(ipAccessNode, databaseName, collectionName):
    command = "echo -e \"use " + databaseName + " ;\n db." + collectionName + ".remove({})\" | mongo "  # execute on mongod
    executeShellCommand(ipAccessNode, command)

def freeUpUnusedSpace(ipDataNodes, databaseName):
    for ip in ipDataNodes:
        command = "echo -e \"use " + databaseName + " ;\n db.repairDatabase()\" | mongo --port 27018"  # execute on mongod
        executeShellCommand(ip, command)

def executeShellCommand(ip, shellCommand):
    exitCode = subprocess.call("ssh root@" + ip + " '" + shellCommand + "'", shell=True)
    if exitCode != 0:
        raise Exception("Executing shell command failed: " + shellCommand)
