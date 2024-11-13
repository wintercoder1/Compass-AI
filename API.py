import Util
from DataCache.CassandraDBCache import CassandraDBCache
from DataClassWrappers.TopicInfo import TopicInfo
from LLMQueryEngine import LLMQueryEngine
from fastapi import FastAPI

app = FastAPI()

isProd = False

@app.get("/getPoliticalLeaningWithCitation/{query_topic}")
async def getPoliticalLeaningWithCitation(query_topic):
    # If this was already answered return the cached response and return
    dbCache = CassandraDBCache(prod=isProd)
    most_recent = dbCache.fetchInfoOnTopicMostRecent(query_topic)
    if most_recent != None: # cached answer found.
        print('returning cached response: ')
        json = Util.escapedJsonFromTopicInfo(most_recent)
        print(json)
        return json

    # Otherwise get the LLM response.
    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print('Request received with topic: {query_topic}')
    print('Waiting....')
    response = llmWithCitations.politicalQueryWithCitation(query_topic_str)
    # Format the reponse and parse out the important information.
    response_dataclass:TopicInfo = Util.parsePolitcalLeaingResponse(response, query_topic)
 
    # Save to DB if a properly formatted answer.
    if type(response_dataclass) is TopicInfo: # will be str or null if parse error.
        print('Writing to DB now..')
        dbCache.writeTopicInfoToDB(response_dataclass)
    else: # If the answer cannot be parsed give back the original string.
        return {'response': response_dataclass}
    # Convert to json to give back to client.
    
    json = Util.escapedJsonFromTopicInfo(response_dataclass)
    print()
    print(json)
    return json


# Will not return a citation based off of sources. Won't consider the documents gathered on possible topics.
@app.get("/getPoliticalLeaning/{query_topic}")
async def getPoliticalLeaningWithoutCitation(query_topic):
    # If this was already answered return the cached response and return
    dbCache = CassandraDBCache(dev=isProd)
    most_recent = dbCache.fetchInfoOnTopicMostRecent(query_topic)
    if most_recent != None: # cached answer found.
        print('returning cached response: ')
        json = Util.escapedJsonFromTopicInfo(most_recent)
        print(json)
        return json

    llmQueryEngine = LLMQueryEngine()
    query_topic_str = str(query_topic)
    response = llmQueryEngine.politicalQueryWithOUTCiation(query_topic_str)
    response_dataclass = Util.parsePolitcalLeaingResponse(response, query_topic, citation=False)

    # Save to DB if a properly formatted answer.
    if type(response_dataclass) is TopicInfo: 
        dbCache.writeTopicInfoToDB(response_dataclass)
    else:# If the answer cannot be parsed give back the original string.
        return {'response': response_dataclass}
    
    json = Util.escapedJsonFromTopicInfo(response_dataclass)
    print()
    print(json)
    return json


# Gpu enabled version. Local only. Currently does not fetch citations from index
# Note we wont cache local responses as they won't cost us as much to w.e.
@app.get("/getPoliticalLeaningWithGPU/{query_topic}")
async def getPoliticalLeaningWithoutCitationWithGPU(query_topic):
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
