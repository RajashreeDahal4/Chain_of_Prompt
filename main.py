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

with open("config.json", encoding="utf-8") as file_data:
        config = json.load(file_data)
sentence_embeddings=load_pickle_files(config["saved_filepath"],'embeddings.pkl')
model=load_pickle_files(config["saved_filepath"],'model.pkl')
unique_gcmd_science_keywords=load_pickle_files(config["saved_filepath"],'gcmd_keywords.pkl')

# Faiss IndexFlat2D
d = sentence_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(sentence_embeddings)

#  Authenticate LLM
llm=OpenAI(model_name='gpt-3.5-turbo',openai_api_key="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")

conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferWindowMemory(k=5)
)


query_message=create_query_message(prompt)
first_result=query_gpt(conversation_buf,query_message)

query_result=convert_str_to_dict(first_result['response'])
gcmd_urls = generate_cmr_query(conversation_buf,query_result,model,index,unique_gcmd_science_keywords)

collections=get_collection_ids_from_url_lists(gcmd_urls)
print("The collections are",collections)