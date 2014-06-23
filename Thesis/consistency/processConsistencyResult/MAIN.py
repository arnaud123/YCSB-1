from Thesis.consistency.processConsistencyResult.FileParser import FileParser
from Thesis.consistency.processConsistencyResult.TimeToConsistencyPlot import TimeToConsistencyPlot
from Thesis.consistency.processConsistencyResult.AmountOfSwapsPlot import AmountOfSwapsPlot

INPUT_FILE = '/home/ec2-user/updateRawData';
OUTPUT_FILE = '/home/ec2-user/result';

fileParser = FileParser();
dataAboutConsistency = fileParser.parse(INPUT_FILE);

timeToConsistencyPlot = TimeToConsistencyPlot(dataAboutConsistency);
timeToConsistencyPlot.plotEarliestConsistentcy(OUTPUT_FILE + '_earliest');
timeToConsistencyPlot.plotLatestConsistency(OUTPUT_FILE + '_latest');
timeToConsistencyPlot.plotEarliestAndLatestConsistency(OUTPUT_FILE + '_combined');

amountOfSwapsPlot = AmountOfSwapsPlot(dataAboutConsistency);
amountOfSwapsPlot.plot(OUTPUT_FILE + '_swaps');