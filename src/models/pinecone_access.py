import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv

# Set API credentials
load_dotenv(find_dotenv())
OPENAI_APIKEY = os.environ["OPENAI_APIKEY"]
PINECONE_APIKEY = os.environ["PINECONE_APIKEY"]
PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]

class access_index:
    def __init__(self):      
        #establish link to Pinecone index
        pinecone.init(
            api_key=PINECONE_APIKEY,
            environment=PINECONE_ENVIRONMENT
        )
        index_name = 'test-bot'
        self.index = pinecone.Index(index_name)

        #initialize OpenAI embedding
        model_name = 'text-embedding-ada-002'
        embed = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=OPENAI_APIKEY
        )

        #create vector store
        text_field = "content"
        self.vectorstore = Pinecone(
            self.index, embed.embed_query, text_field
        )
    
    def query(self, query, k):
        results = self.vectorstore.similarity_search(
            query,
            k=k
        )
        return results
    
    def index_info(self):
        # Get pinecone index info
        return self.index.describe_index_stats()
