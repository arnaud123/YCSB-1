writePlotToFile <- function(x, y, xLabel, yLabel, pathOutputFile){
	png(filename= pathOutputFile);
	plot(x, y, xlab=xLabel, ylab=yLabel);
	# This line draws a vertical,red line at position 5 on the x-axis
	# abline(v=5, col="red")
}

convertSecToMin <- function(sec){
	return(sec/60)
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 2){
 	cat("Usage: script <inputFile> <outputFile>\n")
	quit()
}

pathInputFile = args[1];
pathOutputFile = args[2];

throughput <- read.csv(file=pathInputFile,head=TRUE,sep=",")
timepointsInMin <- convertSecToMin(throughput$sec)
writePlotToFile(timepointsInMin, throughput$throughput, "Minuten", "throughput (ops/sec)", pathOutputFile)