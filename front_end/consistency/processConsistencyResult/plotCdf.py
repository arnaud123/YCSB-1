import subprocess


PATH_TO_PLOT_SCRIPT = '/root/YCSB/front_end/consistency/processConsistencyResult/plotCdf.R'

def plotCdf(dataAboutConsistency, outputFile):
    dataToPlot = dataAboutConsistency.getListTimeToReachConsistency()
    writePlotDataToFile(dataToPlot, outputFile)
    exitCode = subprocess.call(['Rscript', PATH_TO_PLOT_SCRIPT, outputFile, outputFile + '_plot.png'])
    if exitCode != 0:
        raise Exception("Execution of plotscript: \"" + PATH_TO_PLOT_SCRIPT + "\" failed")

def writePlotDataToFile(dataToWrite, outputFile):
    f = open(outputFile, 'w')
    f.write("time_to_reach_consistency\n")
    for item in dataToWrite:
        f.write(str(item) + "\n")
    f.close()