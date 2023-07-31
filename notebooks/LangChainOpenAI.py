import os
from src.apikey import *

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent

import pandas as pd

os.environ['OPENAI_API_KEY'] = OpenAI_apikey

products = pd.read_csv('out.csv')

#LLM
llm = OpenAI(temperature=0)

#Agent
agent = create_pandas_dataframe_agent(llm, products, verbose=True)

st.title('LangChain Test')
prompt = st.text_input('Type in your question!')

#Prompt templates
title_template = PromptTemplate(
    input_variables = ['question'],
    template = '''You are an product specialist at Home Depot who helps customers. 
    
    You: what do you need help with
    
    Customer:{question}'''
)

title_chain = LLMChain(llm=llm, prompt = title_template, verbose = True, )

if prompt:
    answer = agent.run(prompt)
    st.write(answer)
