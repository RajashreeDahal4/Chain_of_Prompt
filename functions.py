import json 
import urllib 
import requests
import streamlit as st

def create_query_message(prompt):
  '''
  This function generates the mesaage to query chatgpt3.5
  returns str: query_message
  '''
  text = input("Enter what you want to search in CMR: ")
  # text=st.text_input("Enter what you want to search in CMR:", key="input")
  query_message = prompt + "Q \"" + text + "\""
  return query_message



def query_gpt(chain,query_message):
  result=chain(query_message)
  return result

def convert_str_to_dict(result):
  return json.loads(result)

def message_phy_obs(keyword):
  message = "Can you give me all the physical observables for " + keyword + " as a python list"
  return message


