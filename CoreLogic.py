from DataCache.CassandraDBCache import CassandraDBCache
from DataClassWrappers.TopicInfo import TopicInfo
from LLMQueryEngine import LLMQueryEngine
from QueryTypeEnum import QueryType
import KnowledgeGraphQueryEngine
import Util

isProd = True

# This method parses the request decides wether to return from cache or not or to call the LLM in citation mode or not.
def parseRequestAndCompleteQuery(query_topic: str, overrideCache:bool=False, withCitation:bool=True):
    print('Query Topic:')
    print(query_topic)
    print()
    dbCache = CassandraDBCache(prod=isProd)
    # If not opted out of Cache response
    if not overrideCache:
        # If this was already answered return the cached response and return
        # Fetch based on normalized topic name. This is meant to reduce deplicates for queries in the DB.
        # It's not a perfect method and that will need to done with something else.
        nomralized_query_topic = Util.normalizeTopicName(query_topic)
        most_recent = dbCache.fetchInfoOnTopicMostRecent(nomralized_query_topic)
        if most_recent != None: # cached answer found.
            print('returning cached response: ')
            json = Util.escapedJsonFromTopicInfo(most_recent, queryType=QueryType.POLITCAL_LEANING, cached=True)
            print(json)
            return json
        else:
            print('not found!')

    # Otherwise get the LLM response.
    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print(f'Request received with topic: {query_topic}')
    print('Waiting....')
    if withCitation:
        response = llmWithCitations.politicalQueryWithCitation(query_topic_str)
    else:
        response = llmWithCitations.politicalQueryWithOUTCitation(query_topic_str)
    # Format the reponse and parse out the important information.
    response_dataclass:TopicInfo = Util.parsePolitcalLeaingResponse(response, query_topic)
    print(response_dataclass)
 
    # Save to DB if a properly formatted answer.
    if type(response_dataclass) is TopicInfo: # will be str or null if parse error.
        print('Writing to DB now..')
        dbCache.writeTopicInfoToDB(response_dataclass)
    else: # If the answer cannot be parsed give back the original string.
        return {'response': response_dataclass}
    # Convert to json to give back to client.
    
    json = Util.escapedJsonFromTopicInfo(response_dataclass, queryType=QueryType.POLITCAL_LEANING, cached=False)
    print()
    print(json)

    return json

def getPoliticalLeaningWithoutCitationWithGPU(query_topic):
    llmQueryEngine = LLMQueryEngine()
    query_topic_str = str(query_topic)
    response = llmQueryEngine.politicalQueryWithGPULocal(query_topic_str)
    response_dataclass = Util.parsePolitcalLeaingResponse(response, query_topic)
    
     # Save to DB if a properly formatted answer.
    if response_dataclass is not TopicInfo:
        return {'response': response_dataclass}
     
    json = Util.escapedJsonFromTopicInfo(response_dataclass)
    print(json)
    return json

# TODO: This shares a ton of logic with 
def parseRequestAndCompleteDEIQuery(query_topic: str, overrideCache:bool=False, withCitation:bool=True):

    dbCache = CassandraDBCache(prod=isProd)
    # # If not opted out of Cache response
    if not overrideCache:
        # If this was already answered return the cached response and return
        nomralized_query_topic = Util.normalizeTopicName(query_topic)
        print('normalized: ' + nomralized_query_topic)
        most_recent = dbCache.fetchInfoOnTopicMostRecent(nomralized_query_topic, queryType=QueryType.DEI_FRIENDLINESS)
        if most_recent != None: # cached answer found.
            print('returning cached response: ')
            json = Util.escapedJsonFromTopicInfo(most_recent, queryType=QueryType.DEI_FRIENDLINESS, cached=True)
            print(json)
            return json
        else:
            print('not found!')

    # Otherwise get the LLM response.
    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print(f'DEI request received with topic: {query_topic}')
    print('Waiting....')
    response = llmWithCitations.deiFriendlinessRatinglQueryWithOUTCitation(query_topic_str)
    # Format the reponse and parse out the important information.
    response_dataclass:TopicInfo = Util.parsePolitcalLeaingResponseDEIOrWokeness(response, query_topic, citation=False)
    print(response_dataclass)
 
    # Save to DB if a properly formatted answer.
    if type(response_dataclass) is TopicInfo: # will be str or null if parse error.
        print('Writing to DB now..')
        dbCache.writeTopicInfoToDB_DEI(response_dataclass)
    else: # If the answer cannot be parsed give back the original string.
        return {'response': response_dataclass}
    # Convert to json to give back to client.
    
    json = Util.escapedJsonFromTopicInfo(response_dataclass, queryType=QueryType.DEI_FRIENDLINESS, cached=False)
    print()
    print(json)

    return json


# TODO: This shares a ton of logic with 
def parseRequestAndCompleteWokenessQuery(query_topic: str, overrideCache:bool=False, withCitation:bool=True):

    dbCache = CassandraDBCache(prod=isProd)
    # # If not opted out of Cache response
    if not overrideCache:
        # If this was already answered return the cached response and return
        nomralized_query_topic = Util.normalizeTopicName(query_topic)
        print('normalized: ' + nomralized_query_topic)
        most_recent = dbCache.fetchInfoOnTopicMostRecent(nomralized_query_topic, queryType=QueryType.WOKENESS)
        if most_recent != None: # cached answer found.
            print('returning cached response: ')
            json = Util.escapedJsonFromTopicInfo(most_recent, queryType=QueryType.WOKENESS, cached=True)
            print(json)
            return json
        else:
            print('not found!')

    # Otherwise get the LLM response.
    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print(f'Wokeness request received with topic: {query_topic}')
    print('Waiting....')
    response = llmWithCitations.deiFriendlinessRatinglQueryWithOUTCitation(query_topic_str)
    # Format the reponse and parse out the important information.
    response_dataclass:TopicInfo = Util.parsePolitcalLeaingResponseDEIOrWokeness(response, query_topic, citation=False)
    print(response_dataclass)
 
    # Save to DB if a properly formatted answer.
    if type(response_dataclass) is TopicInfo: # will be str or null if parse error.
        print('Writing to DB now..')
        dbCache.writeTopicInfoToDB_DEI(response_dataclass)
    else: # If the answer cannot be parsed give back the original string.
        return {'response': response_dataclass}
    # Convert to json to give back to client.
    
    json = Util.escapedJsonFromTopicInfo(response_dataclass, queryType=QueryType.DEI_FRIENDLINESS, cached=False)
    print()
    print(json)

    return json

#
#
# This response will be contained to only the financial contribution data. 
# The LLM will only summarize the data. It won't include the 'opinion' pf the LLM like the other methods.
#
def completeFECFinancialCOntributionsDataQuery(query_topic: str, overrideCache:bool=False):
    #
    # TODO: Implement data cache/persistence for this type of answer. Create new table.
    #

    # 
    # TODO: Fetch financial contributions for company with KnowledgeGrpah (Neo4J)
    #
    file_path = './fec_kg_response_dropbox_pac_example.json'
    financial_contribution_data = Util.load_json(file_path)  ## <---- Replace with query to fetch from knowledge graph DB
    if not financial_contribution_data:
        return {'response': f'Could not find financial contributions from the comapny {topic}'}
    
    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print(f'Wokeness request received with topic: {query_topic}')
    print('Waiting....')
    response = llmWithCitations.deiFriendlinessRatinglQueryWithOUTCitation(query_topic_str, financial_contribution_data)
    return response


def getCachedPolitcalLeaningsEntries():
    return getCachedEntries(QueryType.POLITCAL_LEANING)

def getCachedDEIFriendlinessScoresEntries():
    return getCachedEntries(QueryType.DEI_FRIENDLINESS)

def getCachedWokenessScoresEntries():
    return getCachedEntries(QueryType.WOKENESS)


def getCachedEntries(queryType: QueryType):
    dbCache = CassandraDBCache(prod=isProd)
    row_list = dbCache.fetchInfoAllTopics(queryType=queryType)

    normalized_topic_ids_to_item_map = {}
    for item in row_list:
        n_id = item['normalized_topic_name']
        # If seen before take only the one with most recent timestamp.
        # If lesser timestmap just skip.
        if n_id in normalized_topic_ids_to_item_map:
            prev = normalized_topic_ids_to_item_map[n_id]
            if prev['timestamp'] < item['timestamp']:
                continue
        normalized_topic_ids_to_item_map[n_id] = item

    # normalized topic name could confused end users.
    for _, item in enumerate(normalized_topic_ids_to_item_map.values()):
        del item['normalized_topic_name']

    item_list = list(normalized_topic_ids_to_item_map.values())
    return item_list

if __name__ == "__main__":
    testIsProd = True
    # dbCache = CassandraDBCache(prod=testIsProd)
    # test DB
    # pol_leanings = dbCache.fetchInfoAllTopics(queryType=QueryType.POLITCAL_LEANING)
    # print(pol_leanings)
    #
    # DEI
    # dei_friendliness = dbCache .fetchInfoAllTopics(queryType=QueryType.DEI_FRIENDLINESS)
    # print(dei_friendliness)
    # wokeness = dbCache .fetchInfoAllTopics(queryType=QueryType.WOKENESS)
    # print(wokeness)
    #
    #
    # Financial contributions
    #
    topic = 'Dropbox, Inc'
    financial_contributions = completeFECFinancialCOntributionsDataQuery(query_topic=topic)
    print(financial_contributions)