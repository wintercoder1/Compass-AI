from DataClassWrappers.TopicInfo import TopicInfo
import json
import time

# This is incredibly hacky and not the long term solution. Its only temporary.
# I mean it seriously. This is terrible code and the wrong way to do this. 
# TODO: Rewrite once you get the time. Truly for real pls do.
# TODO: Use dataframes to format the LLM response.
def parsePolitcalLeaingResponse(responseStr: str, topic: str, citation: bool = True) -> TopicInfo | str:
    try:
        split = responseStr.split('lean:')
        
        # Occasioanlly LLMs halucinate and one of the commns ways is to just cut out the Leean field. Idk why.
        # This fixes that occurance.
        no_lean = False
        if len(split) >= 2:
            split = split[1]
        else:
            no_lean = True

        # Rating.
        if not no_lean: ## keep the happy path in the first if and out of the elses
            split = split.split('rating:')
        else :
            split = split[0].split('rating:') 

        if len(split) > 1:
            leanStr = split[0]
            split = split[1]
        else:
            leanStr = split[0].split(':')[0]
            split = split[0]

        # Context
        split = split.split('context:')
        ratingStr = split[0]
        split = split[1]
      
        # Citations.
        if citation:
            split = split.split('citations:')
            if len(split) > 1:
                contextStr = split[0]
                citationStr = split[1]
            else :
                split = split[0].split('Citations:')
                contextStr = split[0]
                if len(split) > 1:
                    citationStr = split[1]
                else:
                    citationStr = 'none'
        else:
            contextStr = split
            citationStr = 'none'
        
        # Wrap up in data class.
        current_timestamp = createTimeStamp()
        rating_int = int(takeOutNonNumeric(ratingStr))

        topicInfo = TopicInfo(
            timestamp = current_timestamp,
            normalized_topic_name = normalizeTopicName(topic),
            topic = topic,
            lean = leanStr,
            rating = rating_int,
            context = contextStr,
            citation = citationStr 
        )

        return topicInfo

    # If output code wont format correctly just return orignial input.
    except IndexError:
        return responseStr
    # except Exception:
    #     return None
 
# Test wether the response string is telling us that the query engine could not fetch relevant documents.
# Note that the query engine halucinates often and returns many false negatives.
# A return type of True means revelant documents or sources were NOT found.
def indexedInfoNotConnectedToTopic(responseStr) -> bool:
    match = (
        responseStr.startswith('There is no relevant information in the provided sources ') or
        responseStr.startswith('I\'m sorry, none of the provided sources contain information about') or 
        responseStr.startswith('I\'m sorry, but the provided sources') or 
        responseStr.startswith('I\'m sorry, but none of the provided sources') or
        responseStr.startswith('Unfortunately, none of the provided sources') or 
        responseStr.startswith('Unfortunately, the provided sources do not') or
        responseStr.startswith('Sorry, none of the provided sources') or 
        responseStr.startswith('I am unable to provide an answer based on the provided sources') or
        responseStr.startswith('There is no information')
    )
    return match

def createTimeStamp() -> int:
    timestamp = int(time.time() * 1000)  # time.time() returns seconds. We multiple by 1000 to get milliseconds
    return timestamp

def takeOutNonNumeric(ini_string: str) -> str:
    getVals = list([val for val in ini_string if val.isdigit()])
    result = "".join(getVals)
    return result

def normalizeTopicName(topic: str) -> str:
    topic = topic.lower() # lower case the string.
    topic = "".join(topic.split()) # take out all whitespace.
    return topic

# Adding this as a constructor to topic info is weird. Idk python is the worst.
def topicInfoFromDict(row_dict: dict) -> TopicInfo:
        current_timestamp = row_dict["timestamp"]
        normalized_topic_name = row_dict["normalized_topic_name"]
        topic = row_dict["topic"]
        lean = row_dict['lean']
        rating = row_dict['rating']
        context = row_dict['context']
        citation = row_dict['citation']
        topicInfo = TopicInfo(
            timestamp = current_timestamp,
            normalized_topic_name = normalized_topic_name,
            topic = topic,
            lean = lean,
            rating = int(rating),
            context = context,
            citation = citation
        )
        return topicInfo

def escapedJsonFromTopicInfo(topicInfo: TopicInfo):
    original_json = topicInfo.to_json()
    print('returning cached response: ')
    # byt defalut this included unneeded escape backslashes. We will take those out.
    epsg_json = json.loads(original_json.replace("\"", '"'))
    return epsg_json

##   
## Test only code
if __name__ == "__main__":
    topic = 'Bud Light'
    normalized_topic_name = 'budlight'
    
    timestamp = int(time.time() * 1000) # time.time() returns seconds. We multiple by 1000 to get milliseconds
    
    leanStr = 'Conservative'
    ratingStr = '3'
    contextStr = 'According to [9], the ' #brand\’s lack of taste differentiation from its ' #closest competitors, such as Coors Light and Miller Light, suggests that the decision to boycott Bud Light by switching to an alternative involves minimal sacrifice in terms of taste preference. This implies that consumers may be more likely to switch to a conservative brand like Coors Light or Miller Light, which are both owned by companies with conservative leanings. However, it\'s worth noting that Bud Light is owned by Anheuser-Busch, which has a liberal leaning [4]. Therefore, the political leaning of Bud Light is conservative, but with a rating of 3, as it is not as conservative as some of its competitors.'
    citationStr = 'In the case of Bud Light' #, the presence of many other light beers on the shelf suggests a high degree of substitutability and low switching costs. This is compounded by the brand\’s lack of taste differentiation from its closest competitors: Blind taste tests on social media show light beer drinkers struggling to distinguish Bud Light from Coors Light and Miller Light. The similarity in flavor profiles among these leading light beer brands suggests that, for consumers, the decision to boycott Bud Light by switching to an alternative like Coors Light or Miller Light involves minimal sacrifice in terms of taste preference.'
   
    topicInfo = TopicInfo.TopicInfo(
        normalized_topic_name = topic,
        topic = topic,
        timestamp = timestamp,
        lean = leanStr,
        rating = int(ratingStr),
        context = contextStr,
        citation = citationStr 
    )
    print(topicInfo)
    topicInfoJSON = topicInfo.to_json()
    print(topicInfoJSON)