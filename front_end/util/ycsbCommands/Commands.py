PATH_YCSB_EXECUTABLE = "bin/ycsb";
TIMESERIES_GRANULARITY = 2000;

FIELD_LENGTH = "100";
FIELD_COUNT = "100";

def getLoadCommand(binding, pathToWorkloadFile, extraParameters = []):
    runCommand = [PATH_YCSB_EXECUTABLE, 'load', binding]; 
    runCommand.extend(['-P', pathToWorkloadFile]);
    runCommand.extend(extraParameters);
    runCommand.extend(['-p', 'fieldlength=' + FIELD_LENGTH]);
    runCommand.extend(['-p', 'fieldcount=' + FIELD_COUNT]);   
    runCommand.extend(['-threads', str(50)]);
    runCommand.append('-s');
    return runCommand;

def getRunCommand(binding, pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters = []):
    runCommand = [PATH_YCSB_EXECUTABLE, 'run', binding]; 
    runCommand.extend(['-P', pathToWorkloadFile]); 
    runCommand.extend(['-p', 'measurementtype=timeseries']); 
    runCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY)]);
    runCommand.extend(['-p', 'maxexecutiontime=' + str(runtimeBenchmarkInMinutes*60)]);
    runCommand.extend(['-p', 'fieldlength=' + FIELD_LENGTH]);
    runCommand.extend(['-p', 'fieldcount=' + FIELD_COUNT]);   
    runCommand.extend(['-threads', amountOfThreads]);
    runCommand.extend(extraParameters);
    runCommand.append('-s');
    return runCommand;
