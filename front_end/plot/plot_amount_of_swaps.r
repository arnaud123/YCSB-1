writePlotToFile <- function(x, y, xLabel, yLabel, pathOutputFile, color){
  png(filename= pathOutputFile);
  plot(x, y, xlab=xLabel, ylab=yLabel, col=color);
}

args <- commandArgs(trailingOnly = TRUE)
argLength <- length(args)
if(argLength != 1){
  cat("Usage: script <inputfile>\n")
  quit()
}
pathInputFile = args[1];

data <- read.csv(file=pathInputFile,head=TRUE,sep=",")
keys <- data$time

for (i in seq(2,length(data)-1)){
  pathOutputFile <- paste(pathInputFile, '_read_thread_', i-2, '_plot.png', sep='')
  writePlotToFile(keys, data[[i]], 'keys', 'amount of swaps', pathOutputFile, 1)
}