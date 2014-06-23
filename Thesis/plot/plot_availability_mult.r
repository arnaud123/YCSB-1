writePlotToFile <- function(x, y, xLabel, yLabel, color, pathOutputFile){
  png(filename= pathOutputFile, width = 700, height = 500)
  plot(x, y, xlab=xLabel, ylab=yLabel, col=color); # ylim=c(0,400000)
  # Draw vertical lines
  abline(v=10, col="red")
  abline(v=15, col="red")
}

addPlot <- function(x, y, color){
	points(x,y, col=color)
}

convertSecToMin <- function(sec){
	return(sec/60)
}

convertMsToMin <- function(ms){
  return(ms/60000)
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 6){
 	cat("Usage: script <throughput> <insertFile> <updateFile> <readFile> <scanFile> <outputFile>\n")
	quit()
}

throughputFile = args[1]
insertFile = args[2];
updateFile = args[3];
readFile = args[4]
scanFile = args[5];
pathOutputFile = args[6];

throughputData <- read.csv(file=throughputFile,head=TRUE,sep=",")
insertData <- read.csv(file=insertFile,head=TRUE,sep=",")
updateData <- read.csv(file=updateFile,head=TRUE,sep=",")
readData <- read.csv(file=readFile,head=TRUE,sep=",")
scanData <- read.csv(file=scanFile,head=TRUE,sep=",")

writePlotToFile(convertSecToMin(throughputData$sec), throughputData$throughput, "Minuten", "throughput (ops/sec)", 1, paste(pathOutputFile, '_throughput_plot.png', sep=''))
writePlotToFile(convertMsToMin(insertData$ms), insertData$latency, "Minuten", "Latency (µs)", 1, paste(pathOutputFile, '_latency_plot.png', sep=''))
addPlot(convertMsToMin(updateData$ms), updateData$latency, 2)
addPlot(convertMsToMin(readData$ms), readData$latency, 3)
addPlot(convertMsToMin(scanData$ms), scanData$latency, 4)

legend("topright", inset=.05, title="Legend", c('Insert', 'Update', 'Read', 'Scan'), col=1:4, pch=1)
