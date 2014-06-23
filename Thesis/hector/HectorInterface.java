import me.prettyprint.cassandra.serializers.StringSerializer;
import me.prettyprint.cassandra.service.template.ColumnFamilyResult;
import me.prettyprint.cassandra.service.template.ColumnFamilyTemplate;
import me.prettyprint.cassandra.service.template.ThriftColumnFamilyTemplate;
import me.prettyprint.hector.api.Cluster;
import me.prettyprint.hector.api.Keyspace;
import me.prettyprint.hector.api.factory.HFactory;

public class HectorInterface {

	private Cluster cluster = null;
	private Keyspace keySpace = null;

	public HectorInterface(String ipAndPort, String clusterName, String keyspaceName) {
		this.cluster = HFactory.getOrCreateCluster(clusterName, ipAndPort);
		this.keySpace = HFactory.createKeyspace(keyspaceName, this.cluster);
	}

	
	// TODO: find a way to convert a string into its hex format
	public ColumnFamilyResult<String, String> read(String key, String columnFamily) {
		ColumnFamilyTemplate<String, String> userCFTemplate = new ThriftColumnFamilyTemplate<String, String>(
				this.keySpace, columnFamily, StringSerializer.get(), StringSerializer.get());
		return userCFTemplate.queryColumns(key);
	}
	
	public static boolean isSameResult(ColumnFamilyResult<String, String> first, ColumnFamilyResult<String, String> second){
		if(first.getColumnNames().size() != second.getColumnNames().size())
			return false;
		for(String columnNameFirst: first.getColumnNames()){
			String valueFirst = first.getString(columnNameFirst);
			String valueSecond = second.getString(columnNameFirst);
			if(valueSecond == null || !valueFirst.equals(valueSecond))
				return false;
		}
		return true;
	}
}