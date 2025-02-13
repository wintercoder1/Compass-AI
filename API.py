from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import CoreLogic

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/getPoliticalLeaningWithCitation/{query_topic}")
async def getPoliticalLeaningWithCitation(query_topic, overrideCache: bool | None = None):
    # return {"message": "Hello, FastAPI!"}
    if overrideCache:
        override = overrideCache
    else:
        override = False

    jsonBody = CoreLogic.parseRequestAndCompleteQuery(query_topic, 
                                                  overrideCache=override, 
                                                  withCitation=True)
    return jsonBody

# Will not return a citation based off of sources. Won't consider the documents gathered on possible topics.
@app.get("/getPoliticalLeaning/{query_topic}")
async def getPoliticalLeaningWithoutCitation(query_topic, overrideCache: bool | None = None):
    #
    if overrideCache:
        override = overrideCache
    else:
        override = False

    jsonBody = CoreLogic.parseRequestAndCompleteQuery(query_topic, 
                                                  overrideCache=override, 
                                                  withCitation=False)
    return jsonBody

@app.get("/getDEIFriendlinessScore/{query_topic}")
async def getDEIFriendlinessScore(query_topic, overrideCache: bool | None = None):
    #
    if overrideCache:
        override = overrideCache
    else:
        override = False
    print('Override: ' + str(override))

    jsonBody = CoreLogic.parseRequestAndCompleteDEIQuery(query_topic, 
                                                     overrideCache=override, 
                                                     withCitation=False)
    return jsonBody

# GPU enabled version. Local only. Currently does not fetch citations from index
# Note we wont cache local responses as they won't cost us as much to w.e.
@app.get("/getPoliticalLeaningWithGPU/{query_topic}")
async def getPoliticalLeaningWithoutCitationWithGPU(query_topic):
    jsonBody = CoreLogic.getPoliticalLeaningWithoutCitationWithGPU(query_topic=query_topic)
    return jsonBody


#
# Cached responses.
#


# TODO: Implement pagination for these two endpoints.
# Returns all previoulsy calculated political leanings.
@app.get("/getCachedPolitcalLeanings")
async def getCachedPolitcalLeaningsAPI():
    jsonBody = CoreLogic.getCachedPolitcalLeaningsEntries()
    return jsonBody

# Returns all previoulsy calculated DEI friendlines scores.
@app.get("/getCachedDEIScores")
async def getCachedDEIFriendlinessScoresAPI():
    jsonBody = CoreLogic.getCachedDEIFriendlinessScoresEntries()
    return jsonBody


# Use this ewith the uvicorn web server.
if __name__ == "__main__":
    uvicorn.run('API:app', host="127.0.0.1", port=8000, reload=True)