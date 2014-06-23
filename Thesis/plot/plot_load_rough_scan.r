writePlotToFile <- function(x, y, amountOfThreads, xLabel, yLabel, pathOutputFile){
	png(filename= pathOutputFile);
	plot(x, y, xlab=xLabel, ylab=yLabel, type="o");
	# Label datapoint with amount of threads used (above)
	text(x, y, amountOfThreads, pos=rep(1, length(amountOfThreads)))
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 2){
 	cat("Usage: script <inputFile> <outputFile>\n")
	quit()
}

pathInputFile = args[1];
pathOutputFile = args[2];

throughputData <- read.csv(file=pathInputFile,head=TRUE,sep=",")
writePlotToFile(throughputData$throughput, throughputData$latency, throughputData$threads, "Throughput (ops/sec)", "latency (µ/s)", pathOutputFile)