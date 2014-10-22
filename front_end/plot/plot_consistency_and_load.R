writeLoadPlot <- function(x, y, xLabel, yLabel, pathOutputFile, color){
  png(filename= pathOutputFile, width=1800, height=1400, res=200);
  # set margins
  par(mar=c(4,4,3,4))
  plot(x, y, xlab="", ylab="", col=color, ylim=c(0,max(y)), type="l");
  points(x,y,col=color)
  # x-axis
  axis(1, xlim=c(0,x),col="black",lwd=2)
  mtext(1,text="throughput (ops/sec)",line=2)
  # y-axis
  axis(2, xlim=c(0,y),col="black",lwd=2)
  mtext(2,text="latency (µs)",line=2)
}

addPlot <- function(x, y, maxYlim, color){
  par(new=T)
  plot(x, y, axes=F, ylim=c(0,maxYlim), xlab="", ylab="",type="l", col=color, main="")
  points(x,y,col=color)
}

addExtraYAxis <- function(maxYlim){
  # lines(x,y, col=color)
  axis(4, ylim=c(0,maxYlim),col="black",lwd=2)
  mtext(4,text="amount of inconsistent reads",line=2)
}

getMaxValue <- function(sequence1, sequence2){
  maxFirstSequence <- max(sequence1)
  maxSecondSequence <- max(sequence2)
  return (max(maxFirstSequence, maxSecondSequence))
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 4){
  cat("Usage: script <loadData> <insertConsistencyData> <updateConsistencyData> <outputFile>\n")
  quit()
}

# get paths to data files
pathLoadData <- args[1];
pathInsertConsistencyData <- args[2];
pathUpdateConsistencyData <- args[3];
pathOutputFile <- args[4]
# Load data in data files
loadData <- read.csv(file=pathLoadData,head=TRUE,sep=",")
insertConsistencyData <- read.csv(file=pathInsertConsistencyData,head=TRUE,sep=",")
updateConsistencyData <- read.csv(file=pathUpdateConsistencyData,head=TRUE,sep=",")
# Determine max Y value consistency data
maxYvalueConsistencyData <- getMaxValue(insertConsistencyData$amountInconsistentReads, updateConsistencyData$amountInconsistentReads)
# Plot
writeLoadPlot(loadData$expected_throughput, loadData$latency, 'throughput (ops/sec)', 'latency (µs)', pathOutputFile, 1)
addPlot(insertConsistencyData$throughput, insertConsistencyData$amountInconsistentReads, maxYvalueConsistencyData, 2)
addPlot(updateConsistencyData$throughput, updateConsistencyData$amountInconsistentReads, maxYvalueConsistencyData, 3)
# Set extra Y axis
addExtraYAxis(maxYvalueConsistencyData)
# Add legend
legendTitles <- vector()
legendTitles[1] <- 'Average operation latency'
legendTitles[2] <- '#inconsistent reads after insert'
legendTitles[3] <- '#inconsistent reads after update'
legend("topleft", inset=.05, title="Legend", legendTitles, col=1:5, lty=1, lwd=2)