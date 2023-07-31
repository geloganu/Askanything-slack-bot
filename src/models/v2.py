import os
from dotenv import load_dotenv, find_dotenv

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import (
    ConversationalRetrievalChain,
    LLMChain
)
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate

from . import pinecone_access

# Load environment variables from .env file
load_dotenv(find_dotenv())
OPENAI_APIKEY = os.environ["OPENAI_APIKEY"]

class chat_bot:
    def __init__(self):
        #pinecone index access and vectorstore
        pinecone_index = pinecone_access.access_index()
        vectorstore = pinecone_index.vectorstore

        template = """Given the following chat history and a follow up question, rephrase the follow up input question to be a standalone question.
        Or end the conversation if it seems like it's done.
        Chat History:\"""
        {chat_history}
        \"""
        Follow Up Input: \"""
        {question}
        \"""
        Standalone question:"""
        
        condense_question_prompt = PromptTemplate.from_template(template)
        
        template = """You are a friendly, conversational retail shopping assistant at Home Depot. Use the provided product names and description to show the shopper whats available, help find what they want, and answer any questions.
        
        It's ok if you don't know the answer.
        Question:\"
        \"""
        
        Helpful Answer:"""
        
        qa_prompt= PromptTemplate.from_template(template)
        
        llm = OpenAI(temperature=0.2,openai_api_key=OPENAI_APIKEY,)
 
        streaming_llm = OpenAI(
            openai_api_key=OPENAI_APIKEY,
            streaming=True,
            callback_manager=CallbackManager([
                StreamingStdOutCallbackHandler()
            ]),
            verbose=True,
            max_tokens=500,
            temperature=0.2
        )
        
        # use the LLM Chain to create a question creation chain
        question_generator = LLMChain(
            llm=llm,
            prompt=condense_question_prompt
        )
        
        # use the streaming LLM to create a question answering chain
        doc_chain = load_qa_chain(
            llm=streaming_llm,
            chain_type="stuff",
            prompt=qa_prompt
        )
        
        self.chatbot = ConversationalRetrievalChain(
            retriever=vectorstore.as_retriever(),
            combine_docs_chain=doc_chain,
            question_generator=question_generator
        )
        
        self.chat_history = []

    def chat_query(self, query):
        result = self.chatbot({'question': query, 'chat_history': self.chat_history})
        self.chat_history.append((result['question'], result['answer']))
        return result['answer']
