import json
from fastapi import FastAPI
from LLMQueryEngine import LLMQueryEngine

app = FastAPI()

@app.get("/getPoliticalLeaningWithCitation/{query_topic}")
async def getPoliticalLeaningWithCitation(query_topic):

    llmWithCitations = LLMQueryEngine()
    query_topic_str = str(query_topic)
    print('Request received with topic: {query_topic}')
    print('Waiting....')

    resposne = llmWithCitations.politicalQueryWithCitationLocal(query_topic_str)
    split = resposne.split('Lean:')

    if len(split) > 1:
        split = split[1]
    else:
        split = split[0]
    split = split.split('Rating:')
    leanStr = split[0]

    split = split[1]
    split = split.split('Context:')
    ratingStr = split[0]

    split = split[1]
    split = split.split('Citations:')
    contextStr = split[0]

    if len(split) > 0:
        citationStr = split[1]
    else :
        citationStr = 'Citation: None'

    response = {
        'lean': leanStr,
        'number': ratingStr,
        'context': contextStr,
        'citation': citationStr
    }

    print(response)

    return {"Response": response}

# Will not return a citation based off of sources. Won't consider the documents gathered on possible topics.
@app.get("/getPoliticalLeaning/{query_topic}")
async def getPoliticalLeaningWithoutCitation(query_topic):
    llmQueryEngine = LLMQueryEngine()
    query_topic_str = str(query_topic)
    reposne = llmQueryEngine.politicalQueryLocal(query_topic_str)
    return {"Response": reposne}

# Faster gpu enabled version. Currently does not fetch citations from index
@app.get("/getPoliticalLeaningWithGPU/{query_topic}")
async def getPoliticalLeaningWithoutCitationWithGPU(query_topic):
    llmQueryEngine = LLMQueryEngine()
    query_topic_str = str(query_topic)
    reposne = llmQueryEngine.politicalQueryLocalWithGPU(query_topic_str)
    return {"Response": reposne}