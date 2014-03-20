package com.yahoo.ycsb.measurements;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Properties;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class ConsistencyMeasurements {
	private Set<ConsistencyOneMeasurement> allMeasurements;
	
	private static final String INSERT_MATRIX_PROPERTY = "insertMatrixExportFile";
	
	private final static String SEPERATOR = ",";

	public ConsistencyMeasurements() {
		this.allMeasurements = new HashSet<ConsistencyOneMeasurement>();
	}

	public void addMeasurement(ConsistencyOneMeasurement measurement) {
		allMeasurements.add(measurement);
	}

	public TreeSet<Long> getAllTimings(OperationType type){
		TreeSet<Long> mergedKeys = new TreeSet<Long>();

		for (ConsistencyOneMeasurement measurement : allMeasurements) {
			mergedKeys.addAll(measurement.getTimes(type));
		}
		return mergedKeys;
	}
	
	public TreeMap<Long, TreeMap<Integer, Long>> exportMeasurements(OperationType type) {
		TreeSet<Long> mergedKeys = getAllTimings(type);

		TreeMap<Long, TreeMap<Integer, Long>> result = new TreeMap<Long, TreeMap<Integer, Long>>();
		for (Long time : mergedKeys) {
			TreeMap<Integer, Long> timeMap = new TreeMap<Integer, Long>();
			for (ConsistencyOneMeasurement measurement : allMeasurements) {
				if (measurement.hasDelay(type, time))
					timeMap.put(measurement.getThreadNumber(),
							measurement.getLastDelay(type, time));

				result.put(time, timeMap);
			}
		}

		return result;
	}
	
	public String exportLastDelaysAsMatrix(final OperationType type){
		return exportString(type, new ExportDelay() {
			
			@Override
			public String export(Long time, ConsistencyOneMeasurement measurement) {
				return Long.toString(measurement.getLastDelay(type, time));
			}
		});
	}
	
	public String exportNbOfDifferentDelaysAsMatrix(final OperationType type){
		return exportString(type, new ExportDelay() {
			
			@Override
			public String export(Long time, ConsistencyOneMeasurement measurement) {
				return Integer.toString(measurement.getNumberOfDelays(type, time));
			}
		});
	}
	
	private String exportString(OperationType type, ExportDelay export){
		String output = "";
		
		// First line with header
		Set<Integer> threadIds = new TreeSet<Integer>();
		output += SEPERATOR;
		
		for(ConsistencyOneMeasurement measurement : allMeasurements){
			threadIds.add(measurement.getThreadNumber());
			output += measurement.getThreadNumber() + SEPERATOR;
		}
		output += "\n";
		
		for(Long time :getAllTimings(type)){
			output += time + SEPERATOR;
			for(ConsistencyOneMeasurement measurement : allMeasurements){
				if(measurement.hasDelay(type, time)){
					output += export.export(time, measurement);
				}
				output += SEPERATOR;
			}
			
			output += "\n";
		}
		
		return output;
	}
	
	public ConsistencyOneMeasurement getNewConsistencyOneMeasurement(){
		ConsistencyOneMeasurement result = new ConsistencyOneMeasurement(allMeasurements.size());
		
		allMeasurements.add(result);
		return result;
	}
	
	private interface ExportDelay{
		public String export(Long time, ConsistencyOneMeasurement measurement);
	}

	public void export(Properties props) {
		System.err.println("STARTING TO EXPORT");
		if(props.getProperty(INSERT_MATRIX_PROPERTY) != null){
			System.err.println("STARTING TO EXPORT-2");

			try {
				PrintWriter out = new PrintWriter(props.getProperty(INSERT_MATRIX_PROPERTY));
				out.println(exportLastDelaysAsMatrix(OperationType.INSERT));
				out.close();
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			System.err.println("ENDING EXPORT");
		}

		
	}
}
