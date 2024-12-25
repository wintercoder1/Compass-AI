DEI_CHECK_KEYSPACE_NAME = 'deicheck'
CREATE_DEICHECK_KEYSPACE = f'CREATE KEYSPACE IF NOT EXISTS {DEI_CHECK_KEYSPACE_NAME} '
WITH_REPLICATION = 'WITH REPLICATION = { \'class\' : \'SimpleStrategy\', \'replication_factor\': 1 }';
CREATE_DEICHECK_KEYSPACE_WITH_REPLICATION = CREATE_DEICHECK_KEYSPACE + WITH_REPLICATION

CREATE_POLITICAL_LEANING_CUSTOMTYPE = """ 
    CREATE TYPE IF NOT EXISTS deicheck.politcal_leaning_answer(
        normalized_topic_name TEXT,
        topic TEXT,
        lean TEXT,
        rating int,
        context TEXT,
        citation TEXT
    );"""

CREATE_POLITICAL_LEANING_TABLE = """
    CREATE TABLE IF NOT EXISTS political_leaning (
        normalized_topic_name TEXT,
        timestamp TIMESTAMP,
        topic TEXT,
        lean TEXT,
        rating int,
        context TEXT,
        citation TEXT,
        PRIMARY KEY (normalized_topic_name, timestamp)
    );"""

# CREATE_DEI_CHECK_TABLE = """
#     CREATE TABLE IF NOT EXISTS dei_friendliness (
#         normalized_topic_name TEXT,
#         timestamp TIMESTAMP,
#         topic TEXT,
#         lean TEXT,
#         rating int,
#         context TEXT,
#         citation TEXT,
#         PRIMARY KEY (normalized_topic_name, timestamp)
#     );"""
CREATE_DEI_CHECK_TABLE = """
    CREATE TABLE IF NOT EXISTS dei_friendliness (
        normalized_topic_name TEXT,
        timestamp TIMESTAMP,
        topic TEXT,
        rating int,
        context TEXT,
        citation TEXT,
        PRIMARY KEY (normalized_topic_name, timestamp)
    );"""

INSERT_POLITICAL_LEANING_INFO_PREPARED = """
    INSERT INTO deicheck.political_leaning (normalized_topic_name, timestamp, topic, lean, rating, context, citation) 
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
INSERT_DEI_CHECK_INFO_PREPARED = """
    INSERT INTO deicheck.dei_friendliness (normalized_topic_name, timestamp, topic, rating, context, citation) 
    VALUES (?, ?, ?, ?, ?, ?);
    """

FETCH_POLITICAL_LEANING_INFO = """
    SELECT * FROM deicheck.political_leaning;
    """
FETCH_POLITICAL_LEANING_INFO_PREPARED = """    
    SELECT * FROM deicheck.political_leaning WHERE normalized_topic_name = ?;
    """
FETCH_POLITICAL_LEANING_INFO_MOST_RECENT_PREPARED = """
    SELECT * FROM deicheck.political_leaning WHERE normalized_topic_name = ? ORDER BY timestamp DESC LIMIT 1;
    """

FETCH_DEI_FRIENDLINESS_INFO = """
    SELECT * FROM deicheck.dei_friendliness;
    """
FETCH_DEI_FRIENDLINESS_INFO_PREPARED = """    
    SELECT * FROM deicheck.dei_friendliness WHERE normalized_topic_name = ?;
    """
FETCH_DEI_FRIENDLINESS_INFO_MOST_RECENT_PREPARED = """
    SELECT * FROM deicheck.dei_friendliness WHERE normalized_topic_name = ? ORDER BY timestamp DESC LIMIT 1;
    """