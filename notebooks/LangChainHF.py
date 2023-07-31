import os
from src.apikey import *

import streamlit as st
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

from langchain.agents import create_pandas_dataframe_agent

import pandas as pd

os.environ['HUGGINGFACEHUB_API_TOKEN'] = HF_apikey

products = pd.read_csv('out.csv')

#LLM
llm = HuggingFaceHub(repo_id='meta-llama/Llama-2-7b', model_kwargs={"temperature":1e-10})


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
