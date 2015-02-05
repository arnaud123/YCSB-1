PATH_YCSB_EXECUTABLE = "bin/ycsb";
TIMESERIES_GRANULARITY = 2000;

def getLoadCommand(binding, pathToWorkloadFile, extraParameters = []):
    runCommand = [PATH_YCSB_EXECUTABLE, 'load', binding]; 
    runCommand.extend(['-P', pathToWorkloadFile]);
    runCommand.extend(extraParameters);
    runCommand.extend(['-threads', str(50)]);
    runCommand.append('-s');
    return runCommand;

def getRunCommand(binding, pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters = []):
    runCommand = [PATH_YCSB_EXECUTABLE, 'run', binding]; 
    runCommand.extend(['-P', pathToWorkloadFile]); 
    runCommand.extend(['-p', 'measurementtype=timeseries']); 
    runCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY)]);
    runCommand.extend(['-p', 'maxexecutiontime=' + str(runtimeBenchmarkInMinutes*60)]);
    runCommand.extend(['-p', 'fieldlength=100']);
    runCommand.extend(['-p', 'fieldcount=100']);   
    runCommand.extend(['-threads', amountOfThreads]);
    runCommand.extend(extraParameters);
    runCommand.append('-s');
    return runCommand;
