from util.util import executeCommandOverSsh

def deleteAllDataInMongoDb(ipAccessNode, ipDataNodes, databaseName, collectionName):
    deleteAllDataInCollection(ipAccessNode, databaseName, collectionName)
    freeUpUnusedSpace(ipDataNodes, databaseName)
    # TODO: add sleeps

def deleteAllDataInCollection(ipAccessNode, databaseName, collectionName):
    command = "echo 'use " + databaseName + ";db." + collectionName + ".remove()' | mongo"  # execute on mongos
    executeCommandOverSsh(ipAccessNode, command)

def freeUpUnusedSpace(ipDataNodes, databaseName):
    for ip in ipDataNodes:
        command = "echo 'use " + databaseName + ";db.repairDatabase()' | mongo --port 27018"  # execute on mongod
        executeCommandOverSsh(ip, command)