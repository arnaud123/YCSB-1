writePlotToFile <- function(x, y, xLabel, yLabel, pathOutputFile, color){
  png(filename=pathOutputFile, width=1800, height=1400, res=200);
  plot(x, y, xlab=xLabel, ylab=yLabel, col=color, type="o");
  #points(x, y, col=color)
}

addPlot <- function(x, y, color){
  #plot(x, y, col=color, type="l");
  lines(x, y, col=color, type="o")
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 3){
  cat("Usage: scipt <listInputFiles> <legend> <pathOutputFile>\n")
  quit()
}
splittedListOfFiles <- strsplit(args[1], ',')[[1]]
pathOutputFile <- args[3]

firstLoop <- (1==1)
for (i in 1:length(splittedListOfFiles)) {
	print(splittedListOfFiles[[i]])
	data <- read.csv(file=splittedListOfFiles[[i]],head=TRUE,sep=",")
	# plot data
	if(firstLoop) {
		writePlotToFile(data$throughput, data$amountInconsistentReads, 'throughput (ops/sec)', 'amount of inconsistent reads', pathOutputFile, i)
		firstLoop <- (1==0)
	} else{
		addPlot(data$throughput, data$amountInconsistentReads, i)
	}
}
# Add legend
legendTitles <-  strsplit(args[2], ',')[[1]]
legend("topleft", inset=.05, title="Legend", legendTitles, col=1:length(splittedListOfFiles), lty=1, lwd=2)