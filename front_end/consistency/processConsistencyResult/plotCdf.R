writePlotToFile <- function(counts, labelCounts, xLabel, yLabel, pathOutputFile){
        png(filename= pathOutputFile);
        barplot(counts, main=NULL, xlab=xLabel, ylab=yLabel, names.arg=labelCounts)
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
writePlotToFile(dataToPlot$percentage_consistent_values, dataToPlot$read_delay_in_micros,
                "Delay of read after write (µs)", "Percentage of consistent reads", pathOutputFile)