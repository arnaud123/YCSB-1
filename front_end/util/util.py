import subprocess;

def checkExitCodeOfProcess(exitCode, errorMessage):
    if exitCode != 0:
        raise Exception(errorMessage + ' (exitcode: ' + str(exitCode) + ')');
    
def executeCommandOverSsh(ipRemoteHost, command):
    exitCode = subprocess.call(["ssh", "root@" + ipRemoteHost, command]);
    checkExitCodeOfProcess(exitCode, "Failed executing remote command: " + command);







