import json 
import urllib 
import requests 

def create_query_message(prompt):
  '''
  This function generates the mesaage to query chatgpt3.5
  returns str: query_message
  '''
  text = input("Enter what you want to search in CMR: ")
  query_message = prompt + "Q \"" + text + "\""

  return query_message

def query_gpt(conversation_buf,query_message):
  result=conversation_buf(query_message)
  return result

def convert_str_to_dict(result):
  return json.loads(result)

def message_phy_obs(keyword):
  message = "Can you give me all the physical observables for " + keyword + " as a python list"
  return message

# bounding boxes
def bounding_boxes(city):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"format": "json"}
    query = {
        "q": city,
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}&{urllib.parse.urlencode(query)}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        bounding_box=data[0]["boundingbox"]
        #writing in the format lower left longitude, lower left latitude, upper right longitude, upper right latitude.
        coordinates=bounding_box[2]+','+bounding_box[0]+','+bounding_box[3]+','+bounding_box[1]
        return coordinates
    else:
        print("Error retrieving data from API.")
        
def gpt_query_science_keywords(result):
  query_list = result.strip('][').split(', ')
  query_list=[i.replace("'","") for i in query_list]
  print(query_list)
  gpt_science_keywords = []
  for keyword in query_list:
    message = message_phy_obs(keyword)
    print(message)
    keyword_result = query_gpt(message)
    print("keyword_result", keyword_result)
    # gpt_science_keywords.append(keyword_result['response'].split(':', 1)[1])
    gpt_science_keywords.append(keyword_result['response'])
  return gpt_science_keywords

def process_gpt_science_keywords(gpt_science_keywords):
  all_keywords_gpt = []
  for sc_key in gpt_science_keywords:
    print(sc_key)
    sc_key = sc_key.strip('][').split(', ')
    sc_key=[i.replace('"','') for i in sc_key]
    for value in sc_key:
      all_keywords_gpt.append(value)
    for key in sc_key:
      print(key)
    print(type(sc_key))
  return list(set(all_keywords_gpt))

def similar_GCMD_keywords(unique_gpt_science_keywords,model,index,unique_gcmd_science_keywords):
  gcmd_mapping = {}
  for keywords in unique_gpt_science_keywords:
    k = 3
    print(keywords)
    print(type(keywords))
    xq = model.encode([keywords])
    D, I = index.search(xq, k)
    embeddings_gcmd_keywords = []
    science_list = []
    for idx in I[0]:
      # if idx < sentence_embeddings.shape[0]:
      science_list.append(unique_gcmd_science_keywords[idx])
    gcmd_mapping[keywords] = science_list
  return gcmd_mapping