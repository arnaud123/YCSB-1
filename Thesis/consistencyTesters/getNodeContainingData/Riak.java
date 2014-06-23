import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class Riak {

	private static final String PATH_TO_EXECUTABLE = "/home/ec2-user/bla.py";
	
	public List<String> getIpsOfNodesContaingingDate(String key){
		String output = this.getProcessOutput(key);
		return this.ParseOutputToIps(output);
	}
	
	private String getProcessOutput(String key){
			String threeCommands[] = {"python", PATH_TO_EXECUTABLE, key};
			ProcessBuilder builder = new ProcessBuilder(threeCommands);
			builder.redirectErrorStream();
			Process subProcess = null;
			try {
				subProcess = builder.start();
				subProcess.waitFor();
				return this.getOutput(subProcess);
			} catch (IOException e) {
				e.printStackTrace();
				System.exit(1);
			} catch (InterruptedException e) {
				e.printStackTrace();
				System.exit(1);
			}
			throw new RuntimeException("Fault in subprocess");
	}
	
	private String getOutput(Process process) throws IOException{
		BufferedReader subProcessInputReader = new BufferedReader(
				new InputStreamReader(process.getInputStream()));
		String output= "";
		String line = null;
		while ((line = subProcessInputReader.readLine()) != null)
			output += line;
		subProcessInputReader.close();
		return output;
	}
	
	private List<String> ParseOutputToIps(String outputToParse){
		int startIndex = outputToParse.indexOf("[");
		int endIndex = outputToParse.indexOf("]");
		// get part within [...]
		String ipPartOuput= outputToParse.substring(startIndex+1, endIndex);
		List<String> result = new ArrayList<String>();
		while(true){
			// get first entry ipPartOuput
			int endIndxCurly = ipPartOuput.indexOf("}");
			String oneEntry = ipPartOuput.substring(1, endIndxCurly);
			// Extract ip address
			String[] parts = oneEntry.split(",");
			String hostAndIp = parts[1].substring(1, parts[1].length()-1);
			String ip = hostAndIp.split("@")[1];
			result.add(ip);
		    // Reduce ipPartOuput
			if(ipPartOuput.length() < endIndxCurly+2)
				break;
			ipPartOuput = ipPartOuput.substring(endIndxCurly+2);
		}
		return result;
	}
	
	public static void main(String args[]) {
		Riak riak = new Riak();
		List<String> ips = riak.getIpsOfNodesContaingingDate("arnaud");
		for(String ip: ips){
			System.out.println("#" + ip + "#");
		}
	}
	
}
