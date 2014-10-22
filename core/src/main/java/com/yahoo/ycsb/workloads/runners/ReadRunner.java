package com.yahoo.ycsb.workloads.runners;

import java.util.HashMap;
import java.util.HashSet;

import com.yahoo.ycsb.ByteIterator;
import com.yahoo.ycsb.DB;
import com.yahoo.ycsb.measurements.ConsistencyOneMeasurement;
import com.yahoo.ycsb.measurements.OperationType;
import com.yahoo.ycsb.workloads.ConsistencyTestWorkload;

public class ReadRunner implements Runnable {

	private final long expectedValue;
	private final String keyname;
	final HashSet<String> fields;
	private final DB db;
	private final ConsistencyTestWorkload workload;
	private final ConsistencyOneMeasurement oneMeasurement;
	private final OperationType type;
	private final LastReadValue readValue;

	private final long maxDelayBeforeDropQuery;
	private final long timeout;
	private long nextReadTime;
	
	public ReadRunner(OperationType type, long expectedValue,
			String keyname, HashSet<String> fields, DB db,
			ConsistencyTestWorkload workload,
			ConsistencyOneMeasurement oneMeasurement,
			long maxDelayBeforeDropQuery,
			long timeout, 
			boolean stopOnFirstConsistency,
			long startTime) {
		super();
		this.expectedValue = expectedValue;
		this.keyname = keyname;
		this.fields = fields;
		this.db = db;
		this.workload = workload;
		this.oneMeasurement = oneMeasurement;
		this.type = type;
		this.readValue = new LastReadValue();
		this.maxDelayBeforeDropQuery = maxDelayBeforeDropQuery;
		this.nextReadTime = startTime;
		this.timeout = timeout;
	}

	@Override
	public void run() {
		try {
			long start = System.nanoTime() / 1000;
			long relativeStart = start- expectedValue;
			
			if(start > nextReadTime + maxDelayBeforeDropQuery){
				System.err.println("\tDrop of query due of time");
				oneMeasurement.addMeasurement(this.expectedValue,
						this.type, relativeStart, null, null);
				return;
			}
			
			if(start > expectedValue + timeout){
				if(!readValue.checkKey(expectedValue)){
					oneMeasurement.addMeasurement(this.expectedValue,
							this.type, relativeStart, timeout, null);
				}
				return;
			}
			
			// TODO: check of meting in measurement interval ligt
			ByteIterator readValueAsByteIterator = getReadResult();

			long delay = System.nanoTime() / 1000 - this.expectedValue;

			if (readValueAsByteIterator != null) {
				String temp = readValueAsByteIterator.toString().trim();
				long time = Long.parseLong(temp);

				this.oneMeasurement.addMeasurement(this.expectedValue, this.type, relativeStart, 
									Math.min(delay, nextReadTime+maxDelayBeforeDropQuery), time);
				readValue.setKey(time);
			} else {
				this.oneMeasurement.addMeasurement(this.expectedValue, this.type, relativeStart, 
									Math.min(delay, nextReadTime+maxDelayBeforeDropQuery), null);
				readValue.setReadKey(false);
			}
		} catch (Throwable e) {
			e.printStackTrace();
		}

	}

	private ByteIterator getReadResult() {
		HashMap<String, ByteIterator> readResult = new HashMap<String, ByteIterator>();
		String tableName = this.workload.getTableName();
		this.db.read(tableName, this.keyname, this.fields, readResult);
		
		ByteIterator readValueAsByteIterator = readResult.get(this.workload
				.getFieldWithTimestamp());
		return readValueAsByteIterator;
	}
}