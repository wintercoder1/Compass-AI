# This is incredibly hacky and not the long term solution. Its only temporary.
# TODO: Use dataframes to format the LLM response.
def parsePolitcalLeaingResponse(responseStr: str) -> dict:
    try:
        split = responseStr.split('Lean:')

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

        return response

    # If output code wont format correctly just return orignial input.
    except IndexError:
        return responseStr


# Test wether the response string is telling us that the query engine could not fetch relevant documents.
# Note that the query engine halucinates often and returns many false negatives.
# A return type of True means revelant documents or sources were NOT found.
def indexedInfoNotConnectedToTopic(responseStr):
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