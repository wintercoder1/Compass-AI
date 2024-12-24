from fastapi import FastAPI
import uvicorn
import CoreLogic

app = FastAPI()


@app.get("/getPoliticalLeaningWithCitation/{query_topic}")
async def getPoliticalLeaningWithCitation(query_topic, overrideCache: bool | None = None):
    # return {"message": "Hello, FastAPI!"}
    if overrideCache:
        override = overrideCache
    else:
        override = False

    json = CoreLogic.parseRequestAndCompleteQuery(query_topic, 
                                                  overrideCache=override, 
                                                  withCitation=True)
    return json

# Will not return a citation based off of sources. Won't consider the documents gathered on possible topics.
@app.get("/getPoliticalLeaning/{query_topic}")
async def getPoliticalLeaningWithoutCitation(query_topic, overrideCache: bool | None = None):
    #
    if overrideCache:
        override = overrideCache
    else:
        override = False

    json = CoreLogic.parseRequestAndCompleteQuery(query_topic, 
                                                  overrideCache=override, 
                                                  withCitation=False)
    return json

@app.get("/getDEIFriendlinessScore/{query_topic}")
async def getDEIFriendlinessScore(query_topic, overrideCache: bool | None = None):
    #
    # if overrideCache:
    #     override = overrideCache
    # else:
    #     override = False
    override = False

    # json = CoreLogic.parseRequestAndCompleteQuery(query_topic, 
    #                                               overrideCache=override, 
    #                                               withCitation=False)
    json = CoreLogic.parseRequestAndCompleteDEIQuery(query_topic, 
                                                     overrideCache=override, 
                                                     withCitation=False)
    return json

# GPU enabled version. Local only. Currently does not fetch citations from index
# Note we wont cache local responses as they won't cost us as much to w.e.
@app.get("/getPoliticalLeaningWithGPU/{query_topic}")
async def getPoliticalLeaningWithoutCitationWithGPU(query_topic):
    json = CoreLogic.getPoliticalLeaningWithoutCitationWithGPU(query_topic=query_topic)
    return json


# Use this ewith the uvicorn web server.
if __name__ == "__main__":
    uvicorn.run('API:app', host="127.0.0.1", port=8000, reload=True)