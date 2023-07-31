import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain.agents import Tool, initialize_agent
from dotenv import load_dotenv, find_dotenv

from . import pinecone_access

# Load environment variables from .env file
load_dotenv(find_dotenv())
OPENAI_APIKEY = os.environ["OPENAI_APIKEY"]


class chat_bot:
    def __init__(self):
        #pinecone index access and vectorstore
        pinecone_index = pinecone_access.access_index()
        vectorstore = pinecone_index.vectorstore

        #initiate ChatOpenAI LLM
        llm = ChatOpenAI(
            openai_api_key=OPENAI_APIKEY,
            model_name='gpt-3.5-turbo',
            temperature=0.0
        )

        # conversational memory
        conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True
        )

        # retrieval qa chain
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )

        tools = [
            Tool(
                name='Knowledge Base',
                func=qa.run,
                description=(
                    'use this tool when answering general knowledge queries to get '
                    'more information about the topic'
                )
            )
        ]
        PREFIX = '''You are an online e-commerce website chatbot. The customer is asking help to purchase things from Home Depot. Be kind, detailed, and nice. Present queried search result in a nice way to answer user input. Take the given context. When prompted, give product recommendations in provided data and provide URL.
        '''
        
        FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:
        '''
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        '''

        When you have gathered all the information home hardware products, just write it to the user in the form of a chat bot reponse.

        '''
        Thought: Do I need to use a tool? No
        AI: [write a blog post]
        '''
        """
        
        SUFFIX = '''

        Begin!

        Previous conversation history:
        {chat_history}

        Instructions: {input}
        {agent_scratchpad}
        '''

        self.agent = initialize_agent(
            agent='chat-conversational-react-description',
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method='generate',
            memory=conversational_memory,
            agent_kwargs={
                'prefix':PREFIX,
                'format_instructions': FORMAT_INSTRUCTIONS,
                'suffix': SUFFIX
            }
        )

    def chat_query(self, query):
        return self.agent.run(query)
        #to ask question just run agent.run('<query>')