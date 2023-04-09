import json 
import urllib 
import requests 
def create_query_message(promt):
  '''
  This function generates the mesaage to query chatgpt3.5
  returns str: query_message
  '''
  text = input("Enter what you want to search in CMR: ")
  query_message = promt + "Q \"" + text + "\""

  return query_message

def query_gpt(conversation_buf,query_message):
  result=conversation_buf(query_message)
  return result

def convert_str_to_dict(result):
  return json.loads(result)

def message_phy_obs(keyword):
  message = "Can you give me all the physical observables for " + keyword + " as a python list"
  return message


