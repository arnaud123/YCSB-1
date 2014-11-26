import subprocess


PATH_TO_PLOT_SCRIPT = 'front_end/consistency/processConsistencyResult/plotCdf.R'

def plotInconsistencyWindow(consistencydataset, outputFile):
    lines = _composePlotDataFile(consistencydataset)
    _writePlotDataFile(lines, outputFile)
    _executePlotScript(outputFile)

def _executePlotScript(dataFile):
    exitCode = subprocess.call(['Rscript', PATH_TO_PLOT_SCRIPT, dataFile, dataFile + '_plot.png'])
    if exitCode != 0:
        raise Exception("Execution of plotscript: \"" + PATH_TO_PLOT_SCRIPT + "\" failed")

def _composePlotDataFile(consistencydataset):
    lines = []
    lines.append("read_delay_in_micros,percentage_consistent_values,total_values")  # Header
    readDelayToPercentageConsistenciesMap = consistencydataset.getPercentageOfConsistentValuesPerDelayAfterWrite()
    for readDelayInMicros in sorted(readDelayToPercentageConsistenciesMap):
        percentageConsistentValues = readDelayToPercentageConsistenciesMap[readDelayInMicros]
        totalAmountOfMeasurements = consistencydataset.getAmountOfMeasurements(readDelayInMicros)
        lines.append(str(readDelayInMicros) + "," +
                     str(percentageConsistentValues) + "," +
                     str(totalAmountOfMeasurements))
    return lines

def _writePlotDataFile(linesOfFile, outputFile):
    f = open(outputFile, 'w')
    for line in linesOfFile:
        f.write(line + "\n")
    f.close()