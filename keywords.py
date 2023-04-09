from functions import message_phy_obs,query_gpt 

def gpt_query_science_keywords(conversation_buf,result):
  query_list = result.strip('][').split(', ')
  query_list=[i.replace("'","") for i in query_list]
  gpt_science_keywords = []
  for keyword in query_list:
    message = message_phy_obs(keyword)
    keyword_result = query_gpt(conversation_buf,message)
    gpt_science_keywords.append(keyword_result['response'])
  return gpt_science_keywords

def process_gpt_science_keywords(gpt_science_keywords):
    all_keywords_gpt = []
    for sc_key in gpt_science_keywords:
        sc_key = sc_key.strip('][').split(', ')
        sc_key=[i.replace('"','') for i in sc_key]
    for value in sc_key:
        all_keywords_gpt.append(value)
    return list(set(all_keywords_gpt))



def similar_GCMD_keywords(unique_gpt_science_keywords,model,index,unique_gcmd_science_keywords):
  gcmd_mapping = {}
  for keywords in unique_gpt_science_keywords:
    k = 3
    xq = model.encode([keywords])
    D, I = index.search(xq, k)
    embeddings_gcmd_keywords = []
    science_list = []
    for idx in I[0]:
      science_list.append(unique_gcmd_science_keywords[idx])
    gcmd_mapping[keywords] = science_list
  return gcmd_mapping



def get_gcmd_mappings(conversation_buf,result,model,index,unique_gcmd_science_keywords):
    gpt_science_keywords = gpt_query_science_keywords(conversation_buf,result['query'])
    unique_gpt_science_keywords = process_gpt_science_keywords(gpt_science_keywords)
    gcmd_mapping = similar_GCMD_keywords(unique_gpt_science_keywords,model,index,unique_gcmd_science_keywords)
    return gcmd_mapping


def science_keywords_append(gcmd_mapping):
    all_keywords_suggestion = []
    for key in gcmd_mapping:
        keyword_ls = gcmd_mapping[key]
        science_keyword_str = 'science_keywords/'
        flag = False
        for keyword in keyword_ls:

            dictionary = {")": "%29", ".": "%2E", ")/": "%2F)", "/": "%2F", "(": "%28", "+": "%2B", ",": "%2C", "-": "%2D", " ": "%20"}
            for key in dictionary.keys():
                # print(keyword)
                # address = address.upper().replace(key, dictionary[key])
                keyword = keyword.upper().replace(key, dictionary[key])
            if flag == False:
                science_keyword_str = science_keyword_str + keyword
                flag = True
            else:
                science_keyword_str = science_keyword_str + '&science_keyword/' + keyword
        all_keywords_suggestion.append(science_keyword_str)
    return all_keywords_suggestion