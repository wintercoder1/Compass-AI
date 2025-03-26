from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, dotenv_values
import platform
import ssl
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


# GPU enabled version. Local only. Currently does not fetch citations from index
# Note we wont cache local responses as they won't cost us as much to w.e.
@app.get("/getPoliticalLeaningWithGPU/{query_topic}")
async def getPoliticalLeaningWithoutCitationWithGPU(query_topic):
    jsonBody = CoreLogic.getPoliticalLeaningWithoutCitationWithGPU(query_topic=query_topic)
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

@app.get("/getWokenessScore/{query_topic}")
async def getWokenessScore(query_topic, overrideCache: bool | None = None):
    #
    if overrideCache:
        override = overrideCache
    else:
        override = False
    print('Override: ' + str(override))

    jsonBody = CoreLogic.parseRequestAndCompleteWokenessQuery(query_topic, 
                                                            overrideCache=override, 
                                                            withCitation=False)
    return jsonBody

@app.get("/getFinancialContributions/{query_topic}")
async def getFinancialContributions():
    pass

#
# Cached responses.
#


# TODO: Implement pagination for these two endpoints.
# Returns all previoulsy calculated political leanings.
@app.get("/getCachedPoliticalLeanings")
async def getCachedPolitcalLeaningsAPI():
    jsonBody = CoreLogic.getCachedPolitcalLeaningsEntries()
    return jsonBody

# Returns all previoulsy calculated DEI friendlines scores.
@app.get("/getCachedDEIScores")
async def getCachedDEIFriendlinessScoresAPI():
    jsonBody = CoreLogic.getCachedDEIFriendlinessScoresEntries()
    return jsonBody

# Returns all previoulsy calculated DEI friendlines scores.
@app.get("/getCachedWokenessScores")
async def getCachedWokenessScoresAPI():
    jsonBody = CoreLogic.getCachedWokenessScoresEntries()
    return jsonBody

@app.get("/getCachedFinancialContributions/{query_topic}")
async def getCachedFinancialContributions():
    pass

#
# Test Response
#

@app.get("/")
async def testResponseIndex():
    return {'test': 'test'}

@app.get("/testResponse")
async def testResponse():
    return {'test': 'test'}

# Use this with the uvicorn web server.
if __name__ == "__main__":

    # Only dev environment will be 'Darwin'/MacOS.
    isProd = platform.system() != 'Darwin'

    if isProd:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        dotenv = dotenv_values(find_dotenv())
        SSL_CERTIFICATE_PATH=dotenv.get('SSL_CERTIFICATE_PATH')
        SSL_CERTIFICATE_KEY_PATH=dotenv.get('SSL_CERTIFICATE_KEY_PATH')
        ssl_context.load_cert_chain(SSL_CERTIFICATE_PATH, keyfile=SSL_CERTIFICATE_KEY_PATH)
        uvicorn.run('API:app', host="127.0.0.1", port=8000, ssl=ssl_context)
    else:
        uvicorn.run('API:app', host="127.0.0.1", port=8000, reload=True)