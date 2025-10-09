# combine the data from the different countries into one big file/dictionary 

import os
import json
import re


COUNTRIES = ["Japan", "US", "SouthKorea", "China", "Singapore", "Vietnam", "Germany", "France", "UK", "Australia", "Norway", "Bangladesh", "India", "Malaysia", "Taiwan", "Thailand", "Nepal", "Laos", "Mongolia", "SriLanka", "Phillipines", "Denmark", "Canada", "Netherland", "Belgium", "Switzerland", "Spain", "Italy", "Greece", "Ireland"]
keywords = ["%22climate+equity%22", "%22climate+justice%22", "%22nature-based+solutions%22", "%22regenerative+agriculture%22", "%22agroforestry%22", "%22Australian+Bushfires%22", "%22Typhoon+Hagibis%22", "%22Henan+Floods%22", "%22climate+resilience%22", "%22climate+adaptation%22", '%22green+infrastructure%22']

# COUNTRIES = ["China", "US"]
# keywords = ["%22climate+justice%22", "%22climate+equity%22"]
# keywords = ["%22climate+adaptation%22", "%22climate+resilience%22"]


keyword_to_searchable_keyword = {
    "%22agroforestry%22": "agroforestry",
    "%22Australian+Bushfires%22": "Australian Bushfires",
    "%22climate+adaptation%22": "climate adaptation",
    "%22climate+equity%22": "climate equity",
    "%22climate+justice%22": "climate justice",
    "%22climate+resilience%22": "climate resilience",
    "%22green+infrastructure%22": "green infrastructure",
    "%22hurricane+katrina%22": "hurricane katrina",
    "%22nature-based+solutions%22": "nature-based solutions",
    "%22regenerative+agriculture%22": "regenerative agriculture",
    "%22Typhoon+Hagibis%22": "Typhoon Hagibis",
    "%22Henan+Floods%22": "Henan Floods"
}



def extract_readable_data(list_of_dicts, keyword):
    list_of_readable_dicts = []
    for idx, data_dict in enumerate(list_of_dicts): 
        text_data = data_dict["Document_Content"]
        publisher = data_dict["Source_Name"]
        # extract the data between the title tags in the text_data
        title = re.search(r'<title>(.*?)</title>', text_data)
        if title:
            title = title.group(1)
        else:
            title = ""
        # extract the data between the published tags in the text_data
        published = re.search(r'<published>(.*?)</published>', text_data)
        if published:
            published = published.group(1)
        else:
            published = ""
        # extract the data between the bodyText tags in the text_data (there might be many so i want to aggregate all the search hits together)
        bodyText = re.search(r'<bodyText>(.*?)</bodyText>', text_data)
        if bodyText:
            bodyText = bodyText.group(1)
        else:
            bodyText = ""

        # filter the bodyText for instances
        instances = []
        keywords_freqs = []
        content = bodyText
        search_word = keyword_to_searchable_keyword[keyword]
        # Count occurrences of the keyword (case-insensitive, as a phrase)
        count = len(re.findall(re.escape(search_word), content, re.IGNORECASE))
        keywords_freqs.append((title, count))

        # --- Surrounding context extraction (more than previous and next sentence) ---
        # Remove HTML tags for context extraction
        content_text = re.sub(r'<.*?>', '', content)
        # Split into sentences (simple split on . ! ?)
        # Improved regex: split after punctuation, possibly followed by quotes or tags, and any whitespace or linebreaks
        sentence_splitter = re.compile(r'(?<=[.!?])(?:(?=["\'<])[^A-Za-z0-9]*)?\s*')
        sentences = sentence_splitter.split(content_text)
        # Find all indices where the keyword appears (case-insensitive, as a phrase)
        keyword_pattern = re.compile(re.escape(search_word), re.IGNORECASE)
        context_snippets = []
        for idx, sent in enumerate(sentences):
            if keyword_pattern.search(sent):
                # Get five previous and five next sentences if available
                prev5_sent = sentences[idx-5].strip() if idx > 4 else ""
                prev4_sent = sentences[idx-4].strip() if idx > 3 else ""
                prev3_sent = sentences[idx-3].strip() if idx > 2 else ""
                prev2_sent = sentences[idx-2].strip() if idx > 1 else ""
                prev1_sent = sentences[idx-1].strip() if idx > 0 else ""
                next1_sent = sentences[idx+1].strip() if idx < len(sentences)-1 else ""
                next2_sent = sentences[idx+2].strip() if idx < len(sentences)-2 else ""
                next3_sent = sentences[idx+3].strip() if idx < len(sentences)-3 else ""
                next4_sent = sentences[idx+4].strip() if idx < len(sentences)-4 else ""
                next5_sent = sentences[idx+5].strip() if idx < len(sentences)-5 else ""
                
                snippet_parts = []
                # if prev5_sent:
                #     snippet_parts.append(prev5_sent)
                # if prev4_sent:
                #     snippet_parts.append(prev4_sent)
                # if prev3_sent:
                #     snippet_parts.append(prev3_sent)
                if prev2_sent:
                    snippet_parts.append(prev2_sent)
                if prev1_sent:
                    snippet_parts.append(prev1_sent)
                if next1_sent:
                    snippet_parts.append(next1_sent)
                if next2_sent:
                    snippet_parts.append(next2_sent)
                # if next3_sent:
                #     snippet_parts.append(next3_sent)
                # if next4_sent:
                #     snippet_parts.append(next4_sent)
                # if next5_sent:
                #     snippet_parts.append(next5_sent)
                snippet = " ".join(snippet_parts)
                context_snippets.append(snippet.strip())
        # Output: title, count, and for each instance, the context snippet

        for snippet in context_snippets:
            instances.append(snippet)

        list_of_readable_dicts.append({
            "relevance_score": idx,
            "title": title,
            "published": published[:10],
            "bodyText": bodyText,
            'publisher': publisher, 
            'instances': instances,
        })


    return list_of_readable_dicts


def combine_data():
    for country in COUNTRIES:
        for keyword in keywords:
            combined_data = []
            if country in os.listdir('data'): 
                # read in the json 
                # grab the filename from the list of files within this folder that starts with the keyword
                try: 
                    filename = [f for f in os.listdir(os.path.join('data', country)) if f.startswith(keyword)][0]
                    with open(os.path.join('data', country+'/'+filename), 'r') as f:
                        data = json.load(f)

                    combined_data.extend(extract_readable_data(data, keyword))
                except:
                    pass
            if country+'_1' in os.listdir('data'):
                try: 
                    filename = [f for f in os.listdir(os.path.join('data', country+'_1')) if f.startswith(keyword)][0]
                    with open(os.path.join('data', country+'_1/'+filename), 'r') as f:
                        data = json.load(f)

                    combined_data.extend(extract_readable_data(data, keyword))
                except:
                    pass
            if country+'_2' in os.listdir('data'):
                try: 
                    filename = [f for f in os.listdir(os.path.join('data', country+'_2')) if f.startswith(keyword)][0]
                    with open(os.path.join('data', country+'_2/'+filename), 'r') as f:
                        data = json.load(f)

                    combined_data.extend(extract_readable_data(data, keyword))
                except:
                    pass



            if country+'_3' in os.listdir('data'):
                try: 
                    filename = [f for f in os.listdir(os.path.join('data', country+'_3')) if f.startswith(keyword)][0]
                    with open(os.path.join('data', country+'_3/'+filename), 'r') as f:
                        data = json.load(f)
                    combined_data.extend(extract_readable_data(data, keyword))
                except:
                    pass
            # make the new directory if it doesn't exist
            if not os.path.exists(os.path.join('data', country+'_2sentence')):
                os.makedirs(os.path.join('data', country+'_2sentence'))
            with open(os.path.join('data', country+'_2sentence/'+keyword+'.json'), 'w') as f:
                json.dump(combined_data, f)


if __name__ == "__main__":
    combine_data()