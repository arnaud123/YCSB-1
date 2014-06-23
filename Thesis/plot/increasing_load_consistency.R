writePlotToFile <- function(x, y, xLabel, yLabel, pathOutputFile, color, upperYLimit){
  png(filename= pathOutputFile, width=1800, height=1400, res=200);
  # plot(x, y, xlab=xLabel, ylab=yLabel, col=color);
  plot(x, y, xlab=xLabel, ylab=yLabel, col=color, ylim=c(0,upperYLimit), type="l");
  points(x,y,col=color)
}

addPlot <- function(x, y, color, upperYlimit){
  # lines(x,y, col=color)
  par(new=T)
  plot(x, y, xlab="", ylab="", axes=FALSE, col=color, ylim=c(0,upperYLimit), type="l");
  points(x,y,col=color)
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 3){
  cat("Usage: script <pathInsertData> <pathUpdateData> <pathOutputFile\n")
  quit()
}
# Get input arguments
pathInsertData <- args[1];
pathUpdateData <- args[2];
pathOutputFile <- args[3];
# Load data
insertData <- read.csv(file=pathInsertData,head=TRUE,sep=",")
updateData <- read.csv(file=pathUpdateData,head=TRUE,sep=",")
# Determine Y-lim
upperYLimit <- max(insertData$amountInconsistentReads, updateData$amountInconsistentReads)
# plot data
writePlotToFile(insertData$throughput, insertData$amountInconsistentReads, 'throughput (ops/sec)', 'amount of inconsistent reads', pathOutputFile, 1, upperYLimit)
addPlot(updateData$throughput, updateData$amountInconsistentReads, 2, upperYLimit)
# Add legend
legendTitles <- vector()
legendTitles[1] <- 'insert operations'
legendTitles[2] <- 'update operations'
legend("topleft", inset=.05, title="Legend", legendTitles, col=1:2, lty=1, lwd=2)