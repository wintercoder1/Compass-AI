#
#  Not implemented yet. Coming soon.
#
#
from KnowledgeGraph import CypherQueries
from neo4j import GraphDatabase, RoutingControl

# NEO4J_URI = "neo4j://localhost:7687"
# NEO4J_CONNECTION_STR = 'bolt://localhost:7687'
NEO4J_URI = 'neo4j://localhost'
AUTH = ("Admin", "Password")

class KnowledgeGraphQueryEngine:

    def __init__(self):
        self.neo4j_driver = self.initNeo4J()
        print(self.neo4j_driver)

    def initNeo4J(self):
        # NEO4J_CONNECTION_STR = 'bolt://localhost:7687'
        # NEO4J_URI = 'neo4j://localhost'
        # AUTH = ("Admin", "Password")
        with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            return driver
        # If driver can not init or connect to DB throw exception.
        raise Exception("Could not connect to Neo4J.")
    
    def getPACWithMatchingCompanyName(self, company_name:str):
        records = self.neo4j_driver.execute_query(CypherQueries.MATCH_PAC)
        return records
    

    def parse_neo4j_result(self, eager_result):
        # Extract the records
        records = eager_result.records
        
        # Initialize a list to store parsed data
        parsed_data = []
        
        # Iterate through records
        for record in records:
            # Get the node from the record
            node = record['n']
            
            # Extract node properties as a dictionary
            properties = dict(node.items())
            
            # Add node metadata
            node_data = {
                'id': node.element_id,
                'labels': list(node.labels),
                'properties': properties
            }
            
            parsed_data.append(node_data)

        return parsed_data


    def parsePACRecordsFromNeo4JResult(self, parsed_data):
        committee_name = parsed_data[0]['properties']['committee_id']
        committee_id = parsed_data[0]['properties']['committee_name']
        return (committee_name, committee_id)
    

    def getCommitteeContributorsWithPacID(self, pac_id):
        records = self.neo4j_driver.execute_query(CypherQueries.MATCH_PAC_ID_COMMITTEE)
        return records