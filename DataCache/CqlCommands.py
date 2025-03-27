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

CREATE_WOKENESS_TABLE = """
    CREATE TABLE IF NOT EXISTS wokeness (
        normalized_topic_name TEXT,
        timestamp TIMESTAMP,
        topic TEXT,
        rating int,
        context TEXT,
        citation TEXT,
        PRIMARY KEY (normalized_topic_name, timestamp)
    );"""

# Make sure this is the correct way. Not tested.
CREATE_FINANCIAL_CONTRIUBTIONS_INFO_TABLE = """
    CREATE TABLE IF NOT EXISTS financial_contributions (
        topic TEXT,
        normalized_topic_name TEXT,
        timestamp TIMESTAMP,
        committee_id INT,
        individual_id INT,
        fec_financial_contributions_summary_text TEXT,
        model_used TEXT,
        date_generated DATE,
        PRIMARY KEY (normalized_topic_name, timestamp)
    );"""

# INSERT_POLITICAL_LEANING_INFO_PREPARED = """
#     INSERT INTO deicheck.political_leaning (normalized_topic_name, timestamp, topic, lean, rating, context, citation) 
#     VALUES (?, ?, ?, ?, ?, ?, ?);
#     """
# INSERT_DEI_CHECK_INFO_PREPARED = """
#     INSERT INTO deicheck.dei_friendliness (normalized_topic_name, timestamp, topic, rating, context, citation) 
#     VALUES (?, ?, ?, ?, ?, ?);
#     """

INSERT_POLITICAL_LEANING_INFO_PREPARED = """
    INSERT INTO deicheck.political_leaning (normalized_topic_name, timestamp, topic, lean, rating, context, citation) 
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
INSERT_DEI_FRIENDLINESS_INFO_PREPARED = """
    INSERT INTO deicheck.dei_friendliness (normalized_topic_name, timestamp, topic, rating, context, citation) 
    VALUES (?, ?, ?, ?, ?, ?);
    """
INSERT_WOKENESS_INFO_PREPARED = """
    INSERT INTO deicheck.wokeness (normalized_topic_name, timestamp, topic, rating, context, citation) 
    VALUES (?, ?, ?, ?, ?, ?);
    """
INSERT_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED = """
    INSERT INTO deicheck.financial_contributions (topic, normalized_topic_name, timestamp, committee_id, individual_id, fec_financial_contributions_summary_text, model_used, date_generated) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
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

FETCH_WOKENESS_INFO = """
    SELECT * FROM deicheck.wokeness;
    """
FETCH_WOKENESS_INFO_PREPARED = """    
    SELECT * FROM deicheck.wokeness WHERE normalized_topic_name = ?;
    """
FETCH_WOKENESS_INFO_MOST_RECENT_PREPARED = """
    SELECT * FROM deicheck.wokeness WHERE normalized_topic_name = ? ORDER BY timestamp DESC LIMIT 1;
    """


FETCH_FINANCIAL_CONTRIUBTIONS_INFO = """
    SELECT * FROM deicheck.financial_contributions;
    """
FETCH_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED = """    
    SELECT * FROM deicheck.financial_contributions WHERE normalized_topic_name = ?;
    """
FETCH_FINANCIAL_CONTRIUBTIONS_INFO_MOST_RECENT_PREPARED = """
    SELECT * FROM deicheck.financial_contributions WHERE normalized_topic_name = ? ORDER BY timestamp DESC LIMIT 1;
    """