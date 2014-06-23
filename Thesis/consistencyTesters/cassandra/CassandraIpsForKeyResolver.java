import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class CassandraIpsForKeyResolver {

	private final String ipToResolveNodesWithDataItem;
	
	/*
	 * @param ipToResolveNodesWithDataItem:
	 * 			This ip address will be used to resolve the ip addresses
	 * 			of the nodes responsible for data with a certain key. 
	 */
	public CassandraIpsForKeyResolver(String ipToResolveNodesWithDataItem){
		this.ipToResolveNodesWithDataItem = ipToResolveNodesWithDataItem;
	}
	
	/*
	 * Returns a list of ip addresses of nodes responsible for the data-item within the keyspace
	 * keyspace, within the column family columnFamily and with a key keyAsASCII. 
	 */
	public List<String> getIpsForKey(String keyspace, String columnFamily, String keyAsASCII){
		String keyInHexFormat = this.convertStringToHex(keyAsASCII);
		try {
			String command[] = {"nodetool", "-h", this.ipToResolveNodesWithDataItem, "getendpoints", keyspace, columnFamily, keyInHexFormat};
			ProcessBuilder builder = new ProcessBuilder(command);
			builder.redirectErrorStream();
			Process subProcess = builder.start();
			int exitValue = subProcess.waitFor();
			if(exitValue != 0)
				throw new RuntimeException("exitValue nodetool subprocess: " + exitValue);
			return this.getIpsFromOutput(subProcess);
		} catch (Exception e) {
			e.printStackTrace();
		}
		throw new RuntimeException("Could not retrieve nodes for data item: (" + keyspace + "," + columnFamily + "," + keyInHexFormat + ")");
	}
	
	/*
	 * Example output of process:
	 * 
	 * xss =  -ea -javaagent:/usr/share/cassandra/lib/jamm-0.2.5.jar -XX:+UseThreadPriorities 
	 * -XX:ThreadPriorityPolicy=42 -Xms1G -Xmx1G -Xmn200M -XX:+HeapDumpOnOutOfMemoryError -Xss250k
	 * 172.16.33.4
	 * 172.16.33.2
	 * 172.16.33.5
	 */
	private List<String> getIpsFromOutput(Process process) throws IOException{
		BufferedReader processInputReader = new BufferedReader(
					new InputStreamReader(process.getInputStream()));
		String line = null;
		List<String> result = new ArrayList<String>();
		processInputReader.readLine(); // Neglect first line
		while ((line = processInputReader.readLine()) != null)
			result.add(line);
		processInputReader.close();
		return result;
	}
	
	/*
	 * Converts the given string into its
	 * corresponding hex format.
	 */
	private String convertStringToHex(String str) {
		char[] strAsChars = str.toCharArray();
		StringBuffer hex = new StringBuffer();
		for (int i = 0; i < strAsChars.length; i++) {
			hex.append(Integer.toHexString((int) strAsChars[i]));
		}
		return hex.toString();
	}
	
	public static void main(String[] args) {
		CassandraIpsForKeyResolver resolver = new CassandraIpsForKeyResolver("172.16.33.2");
		List<String> ips = resolver.getIpsForKey("test", "testtable", "ab");
		for(String ip: ips)
			System.out.println("IP: " + ip);
	}
}