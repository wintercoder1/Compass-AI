from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from typing import Optional
from DataCache import CqlCommands
from DataClassWrappers.TopicInfo import TopicInfo
from Util import topicInfoFromDict

# TODO: write wrapers for connection to cloud hosted Cassandra.
class CassandraDBCache:

    DEV_LOCALHOST_URL = '127.0.0.1'
    DEV_PORT = '9042'

    def __init__(self, dev=True) -> None:
        # 
        cluster = Cluster(
            [self.DEV_LOCALHOST_URL], # By default connects to localhost.
            port=self.DEV_PORT
        )
        self.session = cluster.connect()
        self.session.row_factory = dict_factory # returns rows as dict
        # Setup
        # These are all with If not exist suffix.
        # If keyspace doesnt exist on localhost create it.
        self.session.execute(CqlCommands.CREATE_DEICHECK_KEYSPACE_WITH_REPLICATION)
        # Set keyspace.
        self.session.set_keyspace(CqlCommands.DEI_CHECK_KEYSPACE_NAME)
        # Create custom type for storing answers.
        self.session.execute(CqlCommands.CREATE_POLITICAL_LEANING_CUSTOMTYPE)
        # Create table that will store a list of answers for each topic.
        self.session.execute(CqlCommands.CREATE_POLITICAL_LEANING_TABLE)
        

    # Write:
    def writeTopicInfoToDB(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        # ie political leaning to political leaning table. dei or wokeness to respective table.
        INSERT = self.session.prepare(CqlCommands.INSERT_POLITICAL_LEANING_INFO_PREPARED)
        self.session.execute(INSERT, 
                             (
                                topicInfo.normalized_topic_name, 
                                topicInfo.timestamp, 
                                topicInfo.topic, 
                                topicInfo.lean, 
                                topicInfo.rating, 
                                topicInfo.context, 
                                topicInfo.citation
                            )
        )
        return

    # Read:
    # Fetch answers.

    # Returns one most recent answe ron topic.
    def fetchInfoOnTopicMostRecent(self, normalized_topic_name: str ) -> Optional[TopicInfo]: #TopicInfo: #Optional[DataClassWrappers.TopicInfo]:
        # search respective table for an answer relating to the topic
        FETCH = self.session.prepare(CqlCommands.FETCH_POLITICAL_LEANING_INFO_MOST_RECENT_PREPARED)
        rows = self.session.execute(FETCH, (normalized_topic_name, ) )
        if not rows:
            return None
        return topicInfoFromDict(row_dict=rows[0]) 
    
    # Returns all answers ever for topic.
    def fetchInfoOnTopic(self, normalized_topic_name: str) -> list:
        FETCH = self.session.prepare(CqlCommands.FETCH_POLITICAL_LEANING_INFO_PREPARED)
        rows = self.session.execute(FETCH, (normalized_topic_name, ) )
        return rows
    
    # Returns all answers on all topics saved in database.
    def fetchInfoAllTopics(self) -> list:
        row = self.session.execute(CqlCommands.FETCH_POLITICAL_LEANING_INFO)
        return row