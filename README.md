# DEICheck.ai
The retrieval augmented generative AI powered app that fuels DEICheck.ai. Uses Llama with Llama Index and Pinecone Vector Database. (Coming soon... for now it uses LLamaIndex default in memory vector store for word embeddings instead.)

### Instructions

Bring your own LLM with weights saved in .gguf format. Place that in a folder in the main directory called weights.

Begin the FastAPI server with the command:

fastapi dev API.py

This will launch the server with the endpoint: getPoliticalLeaningWithCitation/{query_topic}

Replace query topic with whatever you want to know more about polically for example a get request on
{base_url}/getPoliticalLeaningWithCitation/Valvline will tell you about what Valvoline's political leaning is and who they have donated to.
