package com.yahoo.ycsb.workloads;

import java.util.HashSet;
import java.util.concurrent.TimeUnit;

import com.yahoo.ycsb.DB;
import com.yahoo.ycsb.measurements.OperationType;
import com.yahoo.ycsb.workloads.runners.ReadRunner;

public class ReaderWorkload extends ConsistencyTestWorkload{
	
	private long delayBetweenReadThreadsInMicros = 0;
	
	public void doTransactionUpdate(DB db) {
		if(this.firstOperation){
			doTransactionInsert(db);
			this.firstOperation = false;
		} else{
			String dbkey = buildKeyForUpdate();
			this.checkConsistency(OperationType.UPDATE, db, dbkey);
		}
	}
	
	public void setDelayBetweenReadThreads(long delayInMicros){
		this.delayBetweenReadThreadsInMicros = delayInMicros;
	}
	
	public long getDelayBetweenReadTheadsInMicros(){
		return this.delayBetweenReadThreadsInMicros;
	}

	public void doTransactionInsert(final DB db) {
		if(this.firstOperation)
			this.firstOperation = false;
		int keynum = nextKeynum();
		String dbkey = buildKeyName(keynum);
		this.checkConsistency(OperationType.INSERT, db, dbkey);
	}
	
	private void checkConsistency(OperationType type, DB db, String keyname){
		HashSet<String> fields = new HashSet<String>();
		fields.add(FIELD_WITH_TIMESTAMP);
		long currentTiming = System.nanoTime();
		
		long initialDelay = this.nextTimestamp - (currentTiming / 1000) + this.getDelayBetweenReadTheadsInMicros();
		long expectedValue = this.nextTimestamp;
		long startTime = expectedValue + this.getDelayBetweenReadTheadsInMicros();
		
		ReadRunner readrunner = new ReadRunner(type, expectedValue, keyname,
											fields, db, this, this.oneMeasurement, getMaxDelayBeforeDrop(), 
											getTimeOut(), isStopOnFirstConsistency(), startTime);
		
		executor.schedule(readrunner, initialDelay, TimeUnit.MICROSECONDS);
//		ScheduledFuture<?> taskToCancel = executor.scheduleWithFixedDelay(
//				readrunner, initialDelay, delayBetweenConsistencyChecks,
//				TimeUnit.MICROSECONDS);
		
//		readrunner.setTask(taskToCancel);
		this.updateTimestamp();
	}

}