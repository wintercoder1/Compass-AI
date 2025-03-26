from dotenv import find_dotenv, dotenv_values
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

#
# This file a a collection of LLM factory methods and their configurations.
#


# This uses HuggingFace inference endpoint API for remote exection of the LLM.
# It has a free tier that works for development. The paid version will have 
# dedicated resources and higher rate limit.
def configureHFLlamaIndexInferenceRemote():
    dotenv = dotenv_values(find_dotenv())
    HF_INFERENCE_TOKEN = dotenv.get("HF_CLI_INFERENCE_TOKEN")
    # HuggingFaceInferenceAPI is a subclass of LLamaIndex's LLM class as thus can be
    # used with the citation query engine class.
    llm = HuggingFaceInferenceAPI(
        model_name= "meta-llama/Llama-3.3-70B-Instruct",
        # model_name= "meta-llama/Llama-3.1-70B-Instruct",
        temperature=0.1,
        max_tokens=1024,
        token=HF_INFERENCE_TOKEN,  # Optional
    )
    return llm


# TODO Include a config.json file in weights because that is what hugging face wants.
# def configureLlamaTransformersHFWithGPULocal():
#     llama_3_8B_instruct_base_path = 'C:/Users/Steven/Documents/Dev/DEICheck.ai-withGPU/DEICheck.ai/weights/'
#     # Load your local fine-tuned model and tokenizer
#     # model = AutoModelForCausalLM.from_pretrained(llama_3_8B_instruct_path)
#     model = AutoModelForCausalLM.from_pretrained(llama_3_8B_instruct_base_path, device_map = 'cuda')
#     # tokenizer = AutoTokenizer.from_pretrained(llama_3_8B_instruct_tokenizer_path)

#     # Create the HuggingFaceLLM object
#     llm = HuggingFaceLLM(
#         model=model,
#         # tokenizer=tokenizer,
#         context_window=3900,
#         max_new_tokens=256,
#         # device_map="auto"
#         device_map="cuda"
#     )
#     return llm

 