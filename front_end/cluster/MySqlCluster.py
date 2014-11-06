import subprocess;

from util.util import executeCommandOverSsh
from util.util import checkExitCodeOfProcess;
from cluster import Cluster


class MySqlCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster, ipMasterNode, pathToDbPropertiesFile):
        super().__init__(normalBinding, consistencyBinding, nodesInCluster)
        self.__ipMasterNode = ipMasterNode;
        self.__pathToDbPropertiesFile = pathToDbPropertiesFile;
        self.__pathTmpWorkloadFile = '/tmp/tmpWorkloadFile';
        self.__pathDbPropertiesFile = 'jdbc/db_properties';
    
    def __getIpMasterNode(self):
        return self.__ipMasterNode;
    
    def deleteDataInCluster(self):
        exitCode = subprocess.call(['ssh', 'root@' + self.__getIpMasterNode(), 'mysql -u root -e "delete from ycsb_database.usertable;"']);
        checkExitCodeOfProcess(exitCode, 'Failed to delete all MySQL data');

    def getLoadCommand(self, pathToWorkloadFile, extraParameters = []):
        extraParameters = self.__addDbPropertiesAttribute(extraParameters);
        return super(MySqlCluster, self).getLoadCommand(pathToWorkloadFile, extraParameters);

    def getRunCommand(self, pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters = []):
        extraParameters = self.__addDbPropertiesAttribute(extraParameters);
        return super(MySqlCluster, self).getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters);

    def getConsistencyRunCommand(self, pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInSeconds, amountOfThreads, extraParameters = []):
        extraParameters = self.__addDbPropertiesAttribute(extraParameters);
        return super(MySqlCluster, self).getConsistencyRunCommand(pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInSeconds, amountOfThreads, extraParameters);

    def __addDbPropertiesAttribute(self, paramList):
        paramList.append('-P');
        paramList.append(self.__pathToDbPropertiesFile);
        return paramList;

    def doRemoveNode(self, ipNodeToRemove):
        return subprocess.Popen(["ssh", "root@" + ipNodeToRemove, "mysql -u root -e 'slave stop'"]);

    def doAddNode(self, ipNodeToAdd):
        executeCommandOverSsh(ipNodeToAdd, "mysql -u root -e 'slave start'");
        
    def stopNode(self, ipNodeToStop):
        return subprocess.Popen(["ssh", "root@" + ipNodeToStop, "systemctl stop mysqld"]);

    def startNode(self, ipNodeToStart):
        executeCommandOverSsh(ipNodeToStart, "systemctl start mysqld");
        
    def writeDbPropertiesFile(self, remoteYcsbNodes):
        slavesInCluster = self.getNodesInCluster();
        slavesInCluster.remove(self.__getIpMasterNode());
        fileContent = 'db.driver=com.mysql.jdbc.Driver\n' + \
        'db.url=jdbc:mysql://' + self.__getIpMasterNode() + ',' + ','.join(slavesInCluster) + ':3306/ycsb_database\n' + \
        'db.user=ycsb_user\n' + \
        'db.passwd=ycsb_password\n';
        self.writeFileToYcsbNodes(fileContent, remoteYcsbNodes, self.__pathDbPropertiesFile, self.__pathDbPropertiesFile);