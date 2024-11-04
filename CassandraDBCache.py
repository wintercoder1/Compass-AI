from cassandra.cluster import Cluster
import CqlCommands

# TODO: write wrapers for connection to cloud hosted Cassandra.
class CassandraDBCache:

    DEV_LOCALHOST_URL = '127.0.0.1:9042'

    def __init__(self, dev=True) -> None:
        cluster = Cluster(['localhost']) # By default connects to localhost.
        # cluster = Cluster() # By default connects to localhost.
        self.session = cluster.connect()
        # If keyspace doesnt exist on localhost create it.
        self.session.execute(CqlCommands.CREATE_DEI_CHECK_KEYSPACE)
        # Set keyspace.
        self.session.set_keyspace(CqlCommands.DEI_CHECK_KEYSPACE_NAME)

    # TODO: Replace the dict with a proper dataclass.
    def writeAnswerToDB(self,topic: str, answerMap: dict):
        # write LLm answer to the applicate table
        # ie political leaning to political leaning table. dei or wokeness to respective table.
        # may need to be a prepared statement.
        self.session.execute(CqlCommands.INSERT_POLITICAL_LEANING_INFO)
        return 0


    def topicIsContainedInDB(self, topic: str) -> list:
        # search respective table for an answer relating to the topic
        rows = self.session.execute(CqlCommands.FETCH_POLITICAL_LEANING_INFO)
        return rows #?