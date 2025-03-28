import DataIngestion
import LLMConfig
import Util
from dotenv import find_dotenv, dotenv_values
from PromptTemplates import POLITICAL_LIB_OR_CON_SCORE_PROMPT, DEI_FRIENDLY_SCORE_PROMPT, WOKENESS_SCORE_PROMPT, FEC_FINANICAL_CONTRIBUTION_DATA_OVERVIEW_PROMPT
from llama_index.core import PromptTemplate
from llama_index.core import Settings
from llama_index.core.query_engine import CitationQueryEngine
# 

#
#
# This is a RAG that uses the LLama Index in memory vector store to create a query engine.
#
#
# TODO: Check for documents in index first before querying the query engine.
# TODO: Fall back to non query engine wrapped LLM on case were no relevant documents are found for topic.
# TODO: Replace default vecotr store with Pinecone.
# TODO: Replace default gpt-3.5 with open source Llama model.
# TODO: Create new index for financial data. Use Reciprocal Rerank Fusion Retriever¶:
#       https://docs.llamaindex.ai/en/stable/examples/retrievers/reciprocal_rerank_fusion/#reciprocal-rerank-fusion-retriever
# TODO: Find more test documents. (Later populate these with a web crawler) 
#
class LLMQueryEngine():

    def __init__(self, localLLM=False, withCitation=False) -> None:
        # The LLM version
        # default_cpu_llama_local_llm = LocalLLMFactory.configureLlamaCPP()
        if localLLM:
            llm_to_use = LLMConfig.configureLlamaCPP()
        else:
            llm_to_use = LLMConfig.configureHFLlamaIndexInferenceRemote()
       
        
        
        if withCitation:

            # Only import this if needed. It containes a ton of dependencies taht take a ton of time and storage to download.
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding

            # The embeddings model
            bge_small_embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')
            Settings.embed_model = bge_small_embed_model

            # self.news_document_index = DataIngestion.createNewsDocumentsIndex(reCreateIndex=True)
            self.news_document_index = DataIngestion.createNewsDocumentsIndex(reCreateIndex=False)    
            
            self.citation_query_engine = CitationQueryEngine.from_args(
                self.news_document_index,
                similarity_top_k=2,
                # here we can control how granular citation sources are, the default is 512
                citation_chunk_size=128,
                # llm=default_cpu_llama_local_llm,
                llm=llm_to_use,
            )

        return

    #
    # Takes query topic and perfomrs inference with political leaning prompt.
    # Gives ciations with query engine. 
    # Not 100% accurate yet. Use politicalQueryWithOUTCitation if thats an issue.
    def politicalQueryWithCitation(self, topic):
        prompt_tmpl = PromptTemplate(POLITICAL_LIB_OR_CON_SCORE_PROMPT)
        the_query = prompt_tmpl.format(topic_of_prompt=topic)

        response = self.citation_query_engine.query(the_query)
        responseStr = str(response)

        # If the citation query engine does not return a result (likley due to not having data matching the tpoic in the index)
        # then run a regular old llm query that will not return a citation or sources for its answer.
        # TODO: query the index on the topic first and then only run one of these once.
        if (Util.indexedInfoNotConnectedToTopic(responseStr)):
            response = self.politicalQueryWithOUTCitation(topic)
            citation_string = '\nCitations: None'
            responseStr = str(response) + citation_string
        else:
            # source nodes are 6, because the original chunks of 1024-sized nodes were broken into more granular nodes
            citation_string = '\nCitations:\n' + str(response.source_nodes[0].node.get_text())
            responseStr += citation_string

        return responseStr

    #
    # WithOUT citations. Long term it would be better for the citation model to be the default.
    # These methods wont't technically count as a RAG.
    # These are mostly for testing. politicalQueryWithCitation and variants will make the get consumer facing app. 
    def politicalQueryWithOUTCitation(self, topic):
        prompt_tmpl = PromptTemplate(POLITICAL_LIB_OR_CON_SCORE_PROMPT)
        the_query = prompt_tmpl.format(topic_of_prompt=topic)

        llm = LLMConfig.configureHFLlamaIndexInferenceRemote()
        response = llm.complete(the_query)

        return str(response)

    def deiFriendlinessRatinglQueryWithOUTCitation(self, topic):
            prompt_tmpl = PromptTemplate(DEI_FRIENDLY_SCORE_PROMPT)
            the_query = prompt_tmpl.format(topic_of_prompt=topic)

            llm = LLMConfig.configureHFLlamaIndexInferenceRemote()
            response = llm.complete(the_query)

            return str(response)

    def wokenessRatinglQueryWithOUTCitation(self, topic):
            prompt_tmpl = PromptTemplate(WOKENESS_SCORE_PROMPT)
            the_query = prompt_tmpl.format(topic_of_prompt=topic)

            llm = LLMConfig.configureHFLlamaIndexInferenceRemote()
            response = llm.complete(the_query)

            return str(response)

    #
    #
    # FEC Financial Contribution Data
    #
    #
    def fec_financialContributionsDataQuery(self, topic:str, financial_contribution_data ):
        # Prompt template with topic.
        prompt_tmpl = PromptTemplate(FEC_FINANICAL_CONTRIBUTION_DATA_OVERVIEW_PROMPT)
        # prompt_tmpl = PromptTemplate(RAW_DATA_TEST_PROMPT)
        the_query = prompt_tmpl.format(topic_of_prompt=topic)
        # Append the financial data to the prompt. <---- confirm that this is correct..
        the_query += '\n'
        the_query += 'Financial contribution information:\n'
        the_query += str(financial_contribution_data)

        # print()
        # print(the_query)
        # print()

        llm = LLMConfig.configureHFLlamaIndexInferenceRemote()
        response = llm.complete(the_query)

        return response


#
#
#
# TESTING
#
#
# Test methods to help test the program without running the api server.
# TODO: Put these in a seperate testing only file.
def testWithTopic(topic: str):
    llmWithCitations = LLMQueryEngine()
    response = llmWithCitations.politicalQueryWithCitation(topic)
    return response

def testWithTopicDEI(topic: str):
    llmWithCitations = LLMQueryEngine()
    response = llmWithCitations.deiFriendlinessRatinglQueryWithOUTCitation(topic)
    return response

def testFECFinancialContributionsQuery(topic: str):
    llmWithCitations = LLMQueryEngine()
    output = llmWithCitations.fec_financialContributionsDataQuery(topic)
    return output


if __name__ == "__main__":
    # Test topics
    # topic = "Barnes and Noble"
    # topic = "Black Rifle Coffee"
    # topic = "BP"
    # topic = "Bud Light"
    # topic = 'Jiffy Lube'
    # topic = 'Molson'
    # topic = 'Valvoline'
    # topic = 'Diddy'
    # topic = 'Ghislaine Maxwell'
    # resp = testWithTopic(topic)
    # resp = testWithTopicDEI(topic)
    # resp = testLocalGPU(topic)
    # print('\n' + str(resp) + '\n')


    topic = 'Dropbox, Inc'
    resp = testWithTopicDEI(topic)

    print('\n' + str(resp) + '\n')
