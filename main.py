import json
import openai

import faiss
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from functions import create_query_message,query_gpt,bounding_boxes
import re


from load_files import load_pickle_files
from prompt import prompt

with open("config.json", encoding="utf-8") as file_data:
        config = json.load(file_data)
sentence_embeddings=load_pickle_files(config["saved_filepath"],'embeddings.pkl')
model=load_pickle_files(config["saved_filepath"],'model.pkl')
unique_gcmd_science_keywords=load_pickle_files(config["saved_filepath"],'gcmd_keywords.pkl')

# # non_alphanumeric_keywords = [keyword for keyword in unique_gcmd_science_keywords if re.search(r'[^\w\s]+', keyword)]
# # non_alphanumeric_keywords = [char for string in unique_gcmd_science_keywords for char in re.findall(r'[^\w\s]+', string)]

# # print(list(set(non_alphanumeric_keywords)))

# Faiss IndexFlat2D
d = sentence_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
print(index.is_trained)
index.add(sentence_embeddings)

#  Authenticate LLM
llm=OpenAI(model_name='gpt-3.5-turbo',openai_api_key="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")

conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferWindowMemory(k=5)
)


query_message=create_query_message(prompt)
first_result=query_gpt(conversation_buf,query_message)


coordinates=bounding_boxes("London")
