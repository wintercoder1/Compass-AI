from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra.auth import PlainTextAuthProvider
from cassandra import ConsistencyLevel
from dotenv import find_dotenv, dotenv_values
from typing import Optional
from ssl import SSLContext, PROTOCOL_TLSv1_2 , CERT_REQUIRED, CERT_NONE
from DataCache import CqlCommands
from DataClassWrappers.TopicInfo import TopicInfo
from QueryTypeEnum import QueryType
from Util import topicInfoFromDict

# TODO: write wrapers for connection to cloud hosted Cassandra.
class CassandraDBCache:

    DEV_LOCALHOST_URL = '127.0.0.1'
    DEV_PORT = '9042'

    def __init__(self, prod=False) -> None:
        # Prod configuration
        if prod:
            dotenv = dotenv_values(find_dotenv())
            PROD_URL = dotenv.get('CASSANDRA_KEY_SPACES_AWS_URL')
            PROD_PORT = dotenv.get('CASSANDRA_KEY_SPACES_AWS_PORT')
            AWS_CERT_PATH = dotenv.get('AWS_CERT_PATH_LOCAL')
            # AWS_CERT_PATH = dotenv.get('AWS_CERT_PATH')
            AWS_KEYSPACES_USER_NAME= dotenv.get('AWS_KEYSPACES_USER_NAME')
            AWS_KEYSPACES_PASSWORD= dotenv.get('AWS_KEYSPACES_PASSWORD')
            ## SSL for AWS cert.
            ssl_context = SSLContext(PROTOCOL_TLSv1_2 )
            # TODO: update this to actualy use cert lol.
            ssl_context.verify_mode = CERT_NONE
            # autprovider
            auth_provider = PlainTextAuthProvider(username=AWS_KEYSPACES_USER_NAME, 
                                                  password=AWS_KEYSPACES_PASSWORD
                                                  )

            cluster = Cluster(
                [PROD_URL], # By default connects to localhost.
                ssl_context=ssl_context, 
                auth_provider=auth_provider, 
                port=PROD_PORT
            )
        else:
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
        # Create table that will store a list of answers for each topic.
        # Political leaning DEI and Wokeness will all be seperate tables.
        self.session.execute(CqlCommands.CREATE_POLITICAL_LEANING_TABLE)
        self.session.execute(CqlCommands.CREATE_DEI_CHECK_TABLE)
        

    # Write:
    def writeTopicInfoToDB(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        # ie political leaning to political leaning table. dei or wokeness to respective table.
        # Cassandra managed service requires  local quorum consistency level.
        INSERT = self.session.prepare(CqlCommands.INSERT_POLITICAL_LEANING_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
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
    
    def writeTopicInfoToDB_DEI(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        # ie political leaning to political leaning table. dei or wokeness to respective table.
        # Cassandra managed service requires  local quorum consistency level.
        INSERT = self.session.prepare(CqlCommands.INSERT_DEI_CHECK_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        print(topicInfo)
        self.session.execute(INSERT, 
                             (
                                topicInfo.normalized_topic_name, 
                                topicInfo.timestamp, 
                                topicInfo.topic, 
                                topicInfo.rating, 
                                topicInfo.context, 
                                topicInfo.citation
                            )
        )
        return

    # Read:
    # Fetch answers.

    # Returns one most recent answer on topic.
    def fetchInfoOnTopicMostRecent(self, normalized_topic_name: str, queryType: QueryType = QueryType.POLITCAL_LEANING) -> Optional[TopicInfo]: #TopicInfo: #Optional[DataClassWrappers.TopicInfo]:
        
        # search respective table for an answer relating to the topic.
        if queryType == QueryType.POLITCAL_LEANING:
            FETCH = self.session.prepare(CqlCommands.FETCH_POLITICAL_LEANING_INFO_MOST_RECENT_PREPARED)
        elif queryType == QueryType.DEI_FRIENDLINESS:
            FETCH = self.session.prepare(CqlCommands.FETCH_DEI_FRIENDLINESS_INFO_MOST_RECENT_PREPARED)

        rows = self.session.execute(FETCH, (normalized_topic_name, ) )
        if not rows:
            return None
        return topicInfoFromDict(row_dict=rows[0], queryType=queryType) 
    
    # Returns all answers ever for topic.
    def fetchInfoOnTopic(self, normalized_topic_name: str, queryType: QueryType = QueryType.POLITCAL_LEANING) -> list:
        if queryType == QueryType.POLITCAL_LEANING:
            FETCH = self.session.prepare(CqlCommands.FETCH_POLITICAL_LEANING_INFO_PREPARED)
        elif queryType == QueryType.DEI_FRIENDLINESS:
            FETCH = self.session.prepare(CqlCommands.FETCH_DEI_FRIENDLINESS_INFO_PREPARED)
        rows = self.session.execute(FETCH, (normalized_topic_name, ) )
        return rows
    
    # Returns all answers on all topics saved in database.
    def fetchInfoAllTopics(self, queryType: QueryType) -> list:
        if queryType == QueryType.POLITCAL_LEANING:
            COMMAND = CqlCommands.FETCH_POLITICAL_LEANING_INFO
        elif queryType == QueryType.DEI_FRIENDLINESS:
            COMMAND = CqlCommands.FETCH_DEI_FRIENDLINESS_INFO
        rows = self.session.execute(COMMAND)
        print('rows')
        print(rows)
        return rows