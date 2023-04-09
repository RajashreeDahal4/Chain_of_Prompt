import json 
import urllib
import requests 
import xmltodict 

from keywords import get_gcmd_mappings
from keywords import science_keywords_append

def bbox_append(value , flag = False):
  bbox_str = ''
  if flag == False:
    bbox_str = bbox_str + 'bounding_box[]='+str(value)
  else:
    bbox_str = bbox_str + '&bounding_box[]='+str(value)

  return bbox_str


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
        print(city)
        data = response.json()
        bounding_box=data[0]["boundingbox"]
        #writing in the format lower left longitude, lower left latitude, upper right longitude, upper right latitude.
        coordinates=bounding_box[2]+','+bounding_box[0]+','+bounding_box[3]+','+bounding_box[1]
        return coordinates
    else:
      print("Error retrieving data from API.")
        


def get_cmr_response(url):
  response  = requests.get(url)
  return response.content

def generate_cmr_query(conversation_buf,result,model,index,unique_gcmd_science_keywords):
  baseurl = "https://cmr.earthdata.nasa.gov/search/collections?"
#   flag = False
  query_urls = []
  if result['location']:
    bbox = bounding_boxes(result['location'])

  if result['science_keyword']:
    gcmd_mappings = get_gcmd_mappings(conversation_buf,result,model,index,unique_gcmd_science_keywords) #here
    science_list = science_keywords_append(gcmd_mappings)
    for list_items in science_list:
      query_list_str = '' + list_items
      if result['location']:
        bbox_str = bbox_append(bbox, True)
        query_list_str = query_list_str + bbox_str
        url = baseurl + query_list_str
        query_urls.append(url)

  return query_urls
    
#   if result['location']:
#     value = bounding_boxes(result['location'])
#     baseurl = baseurl + 'bounding_box[]='+str(value)
#     flag = True
#     print('bbox', value)
    
#     # Query back to get physical observables for all query list
#     # print(result['query'])
    
#     # Query back to get physical observables for all query list
#     # print(result['query'])
    
#   #   vlaues
#   #   for loop
#   #   if flag = True:
#   #   baseurl = baseurl + '&' + 'science_keywords\\' + values  
#   #   else:


#   else:
#     print("error")

#   return baseurl, gcmd_mapping




def get_collection_ids_from_url_lists(list_of_urls):
    concept_ids=[]
    names=[]
    locations=[]
    count=0
    for url in list_of_urls:
        response= requests.get(url)
        data_dict=xmltodict.parse(response.content)
        data=json.dumps(data_dict)
        reference=data_dict['results']['references']['reference']
        for i in reference:
            concept_ids.append(i["id"])
            names.append(i["name"])
            locations.append(i["location"])
    return concept_ids,names,locations