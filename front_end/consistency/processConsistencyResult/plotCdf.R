writePlotToFile <- function(x, xLabel, yLabel, pathOutputFile){
        png(filename= pathOutputFile);
        plot(x, xlab=xLabel, ylab=yLabel, main=NULL);
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 2){
        cat("Usage: script <inputFile> <outputFile>\n")
        quit()
}

pathInputFile = args[1];
pathOutputFile = args[2];

dataToPlot <- read.csv(file=pathInputFile,head=TRUE,sep=",")
dataToPlotAsCdf = ecdf(dataToPlot$time_to_reach_consistency)
writePlotToFile(dataToPlotAsCdf, "Time to reach consistency (µs)", "Probability", pathOutputFile)