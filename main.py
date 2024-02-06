import json
import openai

import faiss
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from functions import convert_str_to_dict,create_query_message,query_gpt
import re

from cmr_query import bounding_boxes,generate_cmr_query,get_collection_ids_from_url_lists
from load_files import load_pickle_files
from prompt import prompt

import streamlit as st
from streamlit_chat import message


with open("config.json", encoding="utf-8") as file_data:
        config = json.load(file_data)
sentence_embeddings=load_pickle_files(config["saved_filepath"],'embeddings.pkl')
model=load_pickle_files(config["saved_filepath"],'model.pkl')
unique_gcmd_science_keywords=load_pickle_files(config["saved_filepath"],'gcmd_keywords.pkl')

# Faiss IndexFlat2D
d = sentence_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(sentence_embeddings)


def load_chain():
#  Authenticate LLM
    llm=OpenAI(model_name='gpt-3.5-turbo',openai_api_key="")

    conversation_buf = ConversationChain(
        llm=llm,
        memory=ConversationBufferWindowMemory(k=20)
    )
    return conversation_buf

chain=load_chain()

#Creating the chatbot interface
st.title("chatBot : Streamlit + openAI")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
      text=st.text_input("Enter what you want to search in CMR:", key="input")
      return text

user_input=get_text()

if user_input:
    query_message=create_query_message(prompt,user_input)
    first_result=query_gpt(chain,query_message)
    query_result=convert_str_to_dict(first_result['response'])
    gcmd_urls = generate_cmr_query(chain,query_result,model,index,unique_gcmd_science_keywords)
    collections,names,locations=get_collection_ids_from_url_lists(gcmd_urls)
    names=list(set(names))
        # st.write(collections)
    # # query_message=create_query_message(prompt)
    collection_text="Here are all the collection ids : "+str(collections)
    not_important=query_gpt(chain,collection_text)

    # names_text="Why don't you add these values in your history of names: "+str(names)+ "which in reality is a python list?"
    # not_important=query_gpt(chain,names_text)

    locations_text="Here are all the cmr links for the collection: "+str(locations)
    not_important=query_gpt(chain,locations_text)

    names_text="Here are all the collection names: "+str(names)
    not_important=query_gpt(chain,names_text)

    # second_query_message = input("What else do you need? ")
    second_query_message = st.text_input("What else do you need? ",key="second_input")
    count=0
    while(second_query_message != "exit" and second_query_message != "Exit" and second_query_message):
        response = query_gpt(chain,second_query_message)
        print(chain)
    #   print(inp != "exit" and inp != "Exit")
        # print(response['response'])
        # print(response['response'])
        st.write(response["response"])
        second_query_message = st.text_input("What else do you need?",key=str(count))
        count=count+1
