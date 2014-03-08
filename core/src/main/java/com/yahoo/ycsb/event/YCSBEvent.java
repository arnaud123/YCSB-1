package com.yahoo.ycsb.event;

import java.io.IOException;

import com.yahoo.ycsb.measurements.exporter.MeasurementsExporter;

public class YCSBEvent implements Runnable{
	private final String id;
	private final long startExecutingInMS;
	private final String commands;	
	
	private long delayIn�s;
	private int returnCode;
	
	private boolean isStarted;
	private boolean isExecuted;


	public YCSBEvent(String id, long startExecutingInMS, String commands) {
		super();
		this.id = id;
		this.startExecutingInMS = startExecutingInMS;
		this.commands = commands;
	}

	public long getDelayIn�s() {
		return delayIn�s;
	}

	public boolean isExecuted() {
		return isExecuted;
	}



	public String getId() {
		return id;
	}

	public long getStartExecutingInMS() {
		return startExecutingInMS;
	}

	public String getCommands() {
		return commands;
	}


	public int getReturnCode() {
		return returnCode;
	}

	public boolean isStarted() {
		return isStarted;
	}


	@Override
	public String toString() {
		return "YCSBEvent [id=" + id + ", startExecutingInMS="
				+ startExecutingInMS + ", commands=" + commands
				+ ", delayIn�s=" + delayIn�s + ", returnCode=" + returnCode
				+ ", isStarted=" + isStarted + ", isExecuted=" + isExecuted
				+ "]";
	}

	@Override
	public void run() {
		System.err.println("EVENT" + ", " + getStartExecutingInMS()/1000 + " sec, "
				+ getId() + ", START");
		long startTime = System.nanoTime();
		isStarted = true;
		Runtime rt = Runtime.getRuntime();
		Process pr = null;
		try {
			pr = rt.exec(commands);
			returnCode = pr.waitFor();
		} catch (IOException e) {
			returnCode = -99;
		}catch(InterruptedException e){
			returnCode = -999;
		}finally{
			try{
				pr.destroy();
			}catch(Exception e){}
		}
		
		long endTime = System.nanoTime();
		
		delayIn�s = (endTime-startTime)/1000;
		isExecuted = true;
		System.err.println("EVENT" + ", " + getStartExecutingInMS()/1000 + " sec, "
				+ getId() + ", STOP, execution of " + getDelayIn�s()/1000 + " ms, exitcode " + returnCode);
	}

	public void log(MeasurementsExporter exporter) throws IOException {
		exporter.writeEvent(id, startExecutingInMS, delayIn�s, isStarted, isExecuted, returnCode);
		
	}

	
}

