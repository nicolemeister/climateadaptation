# combine the data from the different countries into one big file/dictionary 
import os
import json
import re
from utils import model


# COUNTRIES = ["Japan", "US", "SouthKorea", "China", "Singapore", "Vietnam", "Germany", "France", "UK", "Australia", "Norway", "Bangladesh", "India", "Malaysia", "Taiwan", "Thailand", "Nepal", "Laos", "Mongolia", "SriLanka", "Phillipines", "Denmark", "Canada", "Netherland", "Belgium", "Switzerland", "Spain", "Italy", "Greece", "Ireland"]
# keywords = ["%22climate+equity%22", "%22climate+justice%22", "%22nature-based+solutions%22", "%22regenerative+agriculture%22", "%22agroforestry%22", "%22Australian+Bushfires%22", "%22Typhoon+Hagibis%22", "%22Henan+Floods%22", "%22climate+resilience%22", "%22climate+adaptation%22", '%22green+infrastructure%22']

COUNTRIES = ["China", "US", "Japan", "UK"]
keywords = ["%22climate+justice%22", "%22climate+equity%22", "%22climate+adaptation%22", "%22climate+resilience%22"]


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



def extract_events(list_of_dicts, keyword, country):
    
    gpt4o_mini = model.Model(model_name="gpt-4o-mini")

    list_of_events = []
    for data_dict in list_of_dicts: 
        title=data_dict["title"]
        published=data_dict["published"]
        bodyText=data_dict["bodyText"]
        publisher=data_dict["publisher"]
        instances=data_dict["instances"]
        # read in the prompt from this path: climateadaptation/prompts
        with open(os.path.join('prompts', 'event_extraction.txt'), 'r') as f:
            prompt = f.read()

        prompt = prompt+bodyText

        event = gpt4o_mini.run_query(prompt)
        print(event)
        list_of_events.append({
            "title": title,
            "published": published,
            "event": event
        })



    return list_of_events


def combine_data():
    for country in COUNTRIES:
        for keyword in keywords:
            combined_data = []
            if country in os.listdir('data'): 
                # read in the json 
                # grab the filename from the list of files within this folder that starts with the keyword
                filename = [f for f in os.listdir(os.path.join('data', country+"_2sentence")) if f.startswith(keyword)][0]
                with open(os.path.join('data', country+"_2sentence", filename), 'r') as f:
                    data = json.load(f)

            
                # extract the events
                event_data = extract_events(data, keyword, country)
                
            # store the data
            combined_data.append({
                "keyword": keyword,
                "country": country,
                "event_data": event_data
            })
            print(combined_data)
            
            if not os.path.exists(os.path.join('data', country+'_event_extracted')):
                os.makedirs(os.path.join('data', country+'_event_extracted'))
            with open(os.path.join('data', country+'_event_extracted/'+keyword+'.json'), 'w') as f:
                json.dump(combined_data, f)


if __name__ == "__main__":
    # combine_data()

    # across all keywords, identify the events that are shared between countries
    country_to_events = {}
    for country in COUNTRIES:
        events = []
        for keyword in keywords:

            with open(os.path.join('data', country+'_event_extracted/'+keyword+'.json'), 'r') as f:
                data = json.load(f)
            for event in data[0]['event_data']:
                if event["event"] != "No Event" and event["event"] not in events:
                    events.append(event["event"])
        country_to_events[country] = {'events': events}

    
    # for each country, identify the events that are shared between the other countries
    for country in COUNTRIES:
        for other_country in COUNTRIES:
            if country != other_country:
                events = country_to_events[country]['events']
                other_events = country_to_events[other_country]['events']
                shared_events = [event for event in events if event in other_events]

                country_to_events[country][other_country] = shared_events
    with open(os.path.join('results', 'country_to_events.json'), 'w') as f:
        json.dump(country_to_events, f)
    print(country_to_events)
                