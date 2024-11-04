DEI_CHECK_KEYSPACE_NAME = 'deicheck'
CREATE_DEI_CHECK_KEYSPACE = 'CREATE KEYSPACE IF NOT EXISTS {DEI_CHECK_KEYSPACE_NAME} WITH REPLICATION = { \'class\' : \'SimpleStrategy\', \'replication_factor\': 1 };'
CREATE_POLITICAL_LEANING_CUSTOMTYPE = """ 
    CREATE TYPE IF NOT EXISTS deicheck.politcal_leaning_answer(
        normalized_name TEXT,
        name TEXT,
        lean TEXT,
        rating: int,
        context: TEXT,
        citations: TEXT
    );"""
CREATE_POLITICAL_LEANING_TABLE = """
    CREATE TABLE IF NOT EXISTS politcal_leaning (
        normalized_name TEXT,
        answer frozen<politcal_leaning_answer>,
        PRIMARY KEY (normalized_name)
    );"""
INSERT_POLITICAL_LEANING_INFO = ''
FETCH_POLITICAL_LEANING_INFO = ''