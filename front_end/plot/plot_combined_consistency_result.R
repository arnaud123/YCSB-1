writePlotToFile <- function(x, y, xLabel, yLabel, pathOutputFile, color){
  png(filename= pathOutputFile, width=1800, height=1400);
  plot(x, y, xlab=xLabel, ylab=yLabel, col=color, ylim=c(0,20000), type="o");
}

addPlot <- function(x, y, color){
  lines(x,y, col=color, type="o")
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

for (i in seq(4,length(data)-2, by=3)){
  pathOutputFile <- paste(pathInputFile, '_read_thread_', (i-1)/3, '_plot.png', sep='')
  titles <- vector()
  titles[1] <- "write start"
  titles[2] <- "write complete"
  titles[3] <- paste('start read thread', (i-1)/3, sep=' ')
  titles[4] <- paste('first consistent thread', (i-1)/3, sep=' ') 
  titles[5] <- paste('all consistent thread', (i-1)/3, sep=' ')
  writePlotToFile(keys, data$Wstart, 'keys', 'time(µs)', pathOutputFile, 1)
  addPlot(keys, data$Wstop, 2)
  addPlot(keys, data[[i]], 3)  
  addPlot(keys, data[[i+1]], 4)
  addPlot(keys, data[[i+2]], 5)
  
  legend("topright", inset=.05, title="Legend", titles, col=1:5, lty=1, lwd=2)
}