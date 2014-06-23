import subprocess;
import time;

DELAY_FOR_IS_FINISHED_CHECK = 10;
REMOTE_RESULT_FILE_PATH = '/root/YCSB/result';

def executeCommandOnYcsbNodes(localCommand, remoteCommand, pathToWriteResultTo, remoteYcsbClientIps):
    resultFile = open(pathToWriteResultTo, 'w');
    localProcess = subprocess.Popen(localCommand, stdout=resultFile);
    remoteProcesses = executeCommandOnRemoteNodes(remoteYcsbClientIps, remoteCommand);
    listOfProcesses = remoteProcesses;
    listOfProcesses.append(localProcess);
    waitForProcessesToFinish(listOfProcesses);
    resultFile.close();
    checkExitCodeOfProcesses(listOfProcesses);
    # TODO: copy remote result file to local

def executeCommandOnRemoteNodes(remoteYcsbClientIps, remoteCommand):
    listOfProcesses = [];
    for ipRemoteMachine in remoteYcsbClientIps:
        joinedRemoteCommand = " ".join(remoteCommand) + ' >' + REMOTE_RESULT_FILE_PATH;
        process = subprocess.Popen(['ssh', 'root@' + ipRemoteMachine, joinedRemoteCommand]);
        listOfProcesses.append(process);
    return listOfProcesses;

def waitForProcessesToFinish(listOfProcesses):
    while containsUnfinishedProcess(listOfProcesses):
        time.sleep(DELAY_FOR_IS_FINISHED_CHECK);

def containsUnfinishedProcess(listOfProcesses):
    for process in listOfProcesses:
        if process.poll() is None:
            return True;
    return False;

def checkExitCodeOfProcesses(listOfProcesses):
    for process in listOfProcesses:
        if process.poll() != 0:
            raise Exception("non-zero exitcode: " + str(process.poll()));