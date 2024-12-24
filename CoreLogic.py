from DataCache.CassandraDBCache import CassandraDBCache
from DataClassWrappers.TopicInfo import TopicInfo
from LLMQueryEngine import LLMQueryEngine
from QueryTypeEnum import QueryType
import Util

isProd = True

# This method parses the request decides wether to return from cache or not or to call the LLM in citation mode or not.
def parseRequestAndCompleteQuery(query_topic: str, overrideCache:bool=False, withCitation:bool=True):

    dbCache = CassandraDBCache(prod=isProd)
    # If not opted out of Cache response
    if not overrideCache:
        # If this was already answered return the cached response and return
        most_recent = dbCache.fetchInfoOnTopicMostRecent(query_topic)
        if most_recent != None: # cached answer found.
            print('returning cached response: ')
            json = Util.escapedJsonFromTopicInfo(most_recent, cached=True)
            print(json)
            return json
        else:
            print('not found!')

    # Otherwise get the LLM response.
    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print('Request received with topic: {query_topic}')
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


def parseRequestAndCompleteDEIQuery(query_topic: str, overrideCache:bool=False, withCitation:bool=True):

    # dbCache = CassandraDBCache(prod=isProd)
    # # If not opted out of Cache response
    # if not overrideCache:
    #     # If this was already answered return the cached response and return
    #     most_recent = dbCache.fetchInfoOnTopicMostRecent(query_topic)
    #     if most_recent != None: # cached answer found.
    #         print('returning cached response: ')
    #         json = Util.escapedJsonFromTopicInfo(most_recent, cached=True)
    #         print(json)
    #         return json
    #     else:
    #         print('not found!')

    # Otherwise get the LLM response.
    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print('Request received with topic: {query_topic}')
    print('Waiting....')
    response = llmWithCitations.deiFriendlinessRatinglQueryWithOUTCitation(query_topic_str)
    # if withCitation:
    #     response = llmWithCitations.politicalQueryWithCitation(query_topic_str)
    # else:
    #     response = llmWithCitations.politicalQueryWithOUTCitation(query_topic_str)
    # Format the reponse and parse out the important information.
    response_dataclass:TopicInfo = Util.parsePolitcalLeaingResponseDEI(response, query_topic, citation=False)
    print(response_dataclass)
 
    # Save to DB if a properly formatted answer.
    if type(response_dataclass) is TopicInfo: # will be str or null if parse error.
        print('Writing to DB now..')
        # dbCache.writeTopicInfoToDB(response_dataclass)
    else: # If the answer cannot be parsed give back the original string.
        return {'response': response_dataclass}
    # Convert to json to give back to client.
    
    json = Util.escapedJsonFromTopicInfo(response_dataclass, queryType=QueryType.DEI_FRIENDLINESS, cached=False)
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