# We give examples of what we want to output to look like. 
# This technique is often given the fancy name ' few-shot prompting'
POLITICAL_LIB_OR_CON_SCORE_PROMPT = (
        "You are the world class expert and judging the political leanings of people and companies."
        " "
        "The rating scale is from 1-5 liberal if they are left leaning or 1-5 conservative if they are on the right."
        "A true neutral a political entity would be a 0."
        " "
        "Examples: "
        " "
        "Taylor Swift: 4 Liberal"
        "Gyslaine Maxwell: 5 Liberal"
        "Frank Delano Roosevelt: 4 Liberal"
        "Budweiser: 4 Liberal"
        "Ted Cruz: 4 conservative "
        "Ted Nugent: 4 conservative "
        "Black Rife Coffee: 5 conservative"
        " "
        " "
        "Format the answer as follows:"
        " "
        "lean: <Direction of lean, either Liberal or conservative >"
        "rating: <insert rating>"
        "context: <insert the reason>"
        " "
        "What is the political leaning of {topic_of_prompt}?"
)


DEI_FRIENDLY_SCORE_PROMPT = (
        "You are a world class expert at judging what people or companies think of DEI. "
        "You are the authority on their DEI friendliness score."
        " "
        "The rating is on a scale of 1-5. 1 means they are racist and do not believe in including other races. "
        "5 means the topic lovse DEI and truly believes in the principles of "
        "Diversity Equity and Inclusion. "
        " "
        "Example:"
        " "
        "Kamala Harris: 5"
        "Blackrock: 5"
        "NFL: 4"
        "Elon Musk: 1"
        "David Sacks: "
        "Chamath: 2"
        " "
        "What is the DEI friendliness rating of {topic_of_prompt}?"
)