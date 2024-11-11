from dotenv import find_dotenv, dotenv_values
from llama_cpp import Llama
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from transformers import AutoModelForCausalLM

#
# This file a a collection of LLM factory methods and their configurations.
#

def configureLlamaCPP():
    llama_3_8B_instruct_base_path = 'weights/'
    llama_3_8B_instruct_path = llama_3_8B_instruct_base_path + 'Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf'

    llm = LlamaCPP(
        # You can pass in the URL to a GGML model to download it automatically
        # model_url=model_url,
        # optionally, you can set the path to a pre-downloaded model instead of model_url
        model_path=llama_3_8B_instruct_path,
        # temperature=1,
        max_new_tokens=128,
        # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
        # context_window=3900,
        # kwargs to pass to __call__()
        generate_kwargs={},
        # kwargs to pass to __init__()
        # set to at least 1 to use GPU
        # model_kwargs={"n_gpu_layers": 1},
        # transform inputs into Llama2 format
        # messages_to_prompt=messages_to_prompt,
        # completion_to_prompt=completion_to_prompt,
        # verbose=True,
        verbose=False,
    )

    return llm

def configureLlamaCPPWithGPU():
    llama_3_8B_instruct_base_path = 'weights/'
    llama_3_8B_instruct_path = llama_3_8B_instruct_base_path + 'Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf'

    gpu_layers = 50 # Change this value based on your model and your GPU VRAM. -1 means full offload to GPU
    llm = Llama(
        model_path=llama_3_8B_instruct_path,
        n_ctx=2048,
        verbose=False,
        n_gpu_layers=gpu_layers,
    )
    return llm

# TODO Include a config.json file in weights because that is what hugging face wants.
def configureLlamaTransformersHFWithGPULocal():
    llama_3_8B_instruct_base_path = 'C:/Users/Steven/Documents/Dev/DEICheck.ai-withGPU/DEICheck.ai/weights/'
    # Load your local fine-tuned model and tokenizer
    # model = AutoModelForCausalLM.from_pretrained(llama_3_8B_instruct_path)
    model = AutoModelForCausalLM.from_pretrained(llama_3_8B_instruct_base_path, device_map = 'cuda')
    # tokenizer = AutoTokenizer.from_pretrained(llama_3_8B_instruct_tokenizer_path)

    # Create the HuggingFaceLLM object
    llm = HuggingFaceLLM(
        model=model,
        # tokenizer=tokenizer,
        context_window=3900,
        max_new_tokens=256,
        # device_map="auto"
        device_map="cuda"
    )
    return llm

# This uses HuggingFace inference endpoint API for remote exection of the LLM.
# It has a free tier that works for development. The paid version will have 
# dedicated resources and higher rate limit.
def configureHFLlamaIndexInferenceRemote():
    dotenv = dotenv_values(find_dotenv())
    HF_INFERENCE_TOKEN = dotenv.get("HF_CLI_INFERENCE_TOKEN")
    # HuggingFaceInferenceAPI is a subclass of LLamaIndex's LLM class as thus can be
    # used with the citation query engine class.
    llm = HuggingFaceInferenceAPI(
        model_name= "meta-llama/Llama-3.1-8B-Instruct",
        # temperature=0.1,
        max_tokens=256,
        token=HF_INFERENCE_TOKEN,  # Optional
    )
    return llm



 