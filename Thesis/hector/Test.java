import static org.junit.Assert.*;
import me.prettyprint.cassandra.service.template.ColumnFamilyResult;

public class Test {

	@org.junit.Test
	public void test() {
		HectorInterface hector = new HectorInterface("localhost:2222", "Test Cluster", "test");
		ColumnFamilyResult<String, String> arnaudResult = hector.read("arnaud", "testtable");
		ColumnFamilyResult<String, String> jochenResult = hector.read("jochen", "testtable");
		ColumnFamilyResult<String, String> ericaResult = hector.read("erica", "testtable");
		// Assert the same
		assertTrue(HectorInterface.isSameResult(arnaudResult, arnaudResult));
		assertTrue(HectorInterface.isSameResult(jochenResult, jochenResult));
		assertTrue(HectorInterface.isSameResult(ericaResult, ericaResult));
		// Assert different
		assertFalse(HectorInterface.isSameResult(arnaudResult, jochenResult));
		assertFalse(HectorInterface.isSameResult(arnaudResult, ericaResult));
		assertFalse(HectorInterface.isSameResult(jochenResult, ericaResult));
	}

}
