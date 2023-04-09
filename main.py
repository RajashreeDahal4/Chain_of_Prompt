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
    llm=OpenAI(model_name='gpt-3.5-turbo',openai_api_key="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")

    conversation_buf = ConversationChain(
        llm=llm,
        memory=ConversationBufferWindowMemory(k=20)
    )
    return conversation_buf

chain=load_chain()


# def get_text():
#       text=st.text_input("Enter what you want to search in CMR:", key="input")
#       return text

# user_input=get_text()

# if user_input:
query_message=create_query_message(prompt)
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

second_query_message = input("What else do you need? ")
while(second_query_message != "exit" and second_query_message != "Exit"):
    response = query_gpt(chain,second_query_message)
#   print(inp != "exit" and inp != "Exit")
    print("The response",response['response'])
    second_query_message = input("What else do you need?")
