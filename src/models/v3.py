import os
from dotenv import load_dotenv, find_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory

from . import pinecone_access

# Load environment variables from .env file
load_dotenv(find_dotenv())
OPENAI_APIKEY = os.environ["OPENAI_APIKEY"]


class chat_bot:
    def __init__(self):
        #pinecone index access and vectorstore
        pinecone_index = pinecone_access.access_index()
        vectorstore = pinecone_index.vectorstore
        retriever = vectorstore.as_retriever()
        
        self.chat_history = []
        
        # Input template
        qa_template = """
        You are a helpful e-commerce chatbot assistant from Home Depot. You have access to Home Depot's database of products with information like product name, description, and price. Use them to suggest products to the customer. Recommend AT MOST 2 products. Write in sentences. Give a description of products in a sentence but BE CONCISE AND SHORT and include the price and url/link. Present chatbot response in a clean and professional manner. If you don't know the answer, just say you don't know. 
        
        If asked a followup question, refer to chat history. Otherwise refer to context.
        
        context: {context}
        =========
        history: {chat_history}
        =========
        question: {question}
        =========
        """
        QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question", "chat_history" ])
        
        # Memory for LLM
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            input_key='question',
            output_key='answer', 
            return_messages=True)
        
        # Initialize ChatOpenAI
        llm = ChatOpenAI(openai_api_key=OPENAI_APIKEY, model_name='gpt-3.5-turbo', temperature=0.1)

        # Initialize conversation QA chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever, 
            memory=memory,
            verbose=True, 
            return_source_documents=True,
            max_tokens_limit=4097, 
            combine_docs_chain_kwargs={'prompt': QA_PROMPT}
            )

    def chat_query(self, query):
        # retuerns query requests and saves input/output to memory.        
        chain_input = {"question": query, "chat_history": self.chat_history}
        result = self.chain(chain_input)
        self.chat_history.append((query, result["answer"]))
        
        return result["answer"]
