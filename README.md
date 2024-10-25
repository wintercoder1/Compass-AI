# DEICheck.ai
The retrieval augmented generative AI powered app that fuels DEICheck.ai. Uses Llama with Llama Index and Pinecone Vector Database. (Coming soon... for now it uses LLamaIndex default in memory vector store for word embeddings instead.)

## Instructions

Bring your own LLM with weights saved in .gguf format. Place that in a folder in the main directory called weights.


### MacOS/Linux
Begin the FastAPI server with the command:

fastapi dev API.py

### GPU acceleration on Windows

In addition to the dependencies in requirements.txt we will need to install Torch with CUDA enabled:

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

(official doc: https://pytorch.org/get-started/locally/)

Set following environment variables:

CMAKE_ARGS = "-DLLAMA_OPENBLAS=on"
FORCE_CMAKE = 1

pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir

Once that is complete the politicalQueryWithOUTCitationLocalWithGPU method will work with the cpu. The response will be 20-30 seconds instead of minutes.

Note for the fasta api server to work on Windows the follow command will need to be ru:


uvicorn API:app --reload

This is a different command than on MacOS/Linux

### Once setup is Complete
This will launch the server with the endpoint: getPoliticalLeaningWithCitation/{query_topic}

Replace query topic with whatever you want to know more about polically for example a get request on
{base_url}/getPoliticalLeaningWithCitation/Valvline will tell you about what Valvoline's political leaning is and who they have donated to.
