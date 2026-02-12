# combine the data from the different countries into one big file/dictionary 

import os
import json
import re
import matplotlib.pyplot as plt

COUNTRIES = ['US_wildfires_1', 'Canada_wildfires_1','Australia_wildfires_1']
COUNTRIES = ['US_wildfires_1']
# keywords = ["%22climate+justice%22", "%22climate+equity%22"]
# keywords = ["%22climate+adaptation%22", "%22climate+resilience%22"]

keywords = ["%22forest+fire%22"]

keyword_to_searchable_keyword = {
    "%22forest+fire%22": "forest fire",

}

def extract_readable_data(country, list_of_dicts, keyword, years, months, titles, published_dates, bodyTexts):
    list_of_readable_dicts = []
    
    for idx, data_dict in enumerate(list_of_dicts): 
        text_data = data_dict["Document_Content"]
        publisher = data_dict["Source_Name"]
        # extract the data between the title tags in the text_data
        try: title = re.search(r'<title>(.*?)</title>', text_data)
        except: continue
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
        year = published.split('-')[0]
        month = published.split('-')[1]

        # extract the data between the bodyText tags in the text_data (there might be many so i want to aggregate all the search hits together)
        bodyText = re.search(r'<bodyText>(.*?)</bodyText>', text_data)
        if bodyText:
            bodyText = bodyText.group(1)
        else:
            bodyText = ""
        
        # extract the data between the <p> and </p> tags and replace with newlines
        p_tags = re.findall(r'<p[^>]*>(.*?)</p>', bodyText)
        if p_tags:
            bodyText = "\n".join(p_tags)

        years[country].append(year)
        months[country].append(month)
        titles[country].append(title)
        published_dates[country].append(published)
        bodyTexts[country].append(bodyText)
        '''
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
        # for idx, sent in enumerate(sentences):
        #     if keyword_pattern.search(sent):
        #         # Get five previous and five next sentences if available
        #         prev5_sent = sentences[idx-5].strip() if idx > 4 else ""
        #         prev4_sent = sentences[idx-4].strip() if idx > 3 else ""
        #         prev3_sent = sentences[idx-3].strip() if idx > 2 else ""
        #         prev2_sent = sentences[idx-2].strip() if idx > 1 else ""
        #         prev1_sent = sentences[idx-1].strip() if idx > 0 else ""
        #         next1_sent = sentences[idx+1].strip() if idx < len(sentences)-1 else ""
        #         next2_sent = sentences[idx+2].strip() if idx < len(sentences)-2 else ""
        #         next3_sent = sentences[idx+3].strip() if idx < len(sentences)-3 else ""
        #         next4_sent = sentences[idx+4].strip() if idx < len(sentences)-4 else ""
        #         next5_sent = sentences[idx+5].strip() if idx < len(sentences)-5 else ""
                
        #         snippet_parts = []
        #         # if prev5_sent:
        #         #     snippet_parts.append(prev5_sent)
        #         # if prev4_sent:
        #         #     snippet_parts.append(prev4_sent)
        #         # if prev3_sent:
        #         #     snippet_parts.append(prev3_sent)
        #         if prev2_sent:
        #             snippet_parts.append(prev2_sent)
        #         if prev1_sent:
        #             snippet_parts.append(prev1_sent)
        #         if next1_sent:
        #             snippet_parts.append(next1_sent)
        #         if next2_sent:
        #             snippet_parts.append(next2_sent)
        #         # if next3_sent:
        #         #     snippet_parts.append(next3_sent)
        #         # if next4_sent:
        #         #     snippet_parts.append(next4_sent)
        #         # if next5_sent:
        #         #     snippet_parts.append(next5_sent)
        #         snippet = " ".join(snippet_parts)
        #         context_snippets.append(snippet.strip())
        # # Output: title, count, and for each instance, the context snippet

        # for snippet in context_snippets:
        #     instances.append(snippet)

        '''

        list_of_readable_dicts.append({
            "relevance_score": idx,
            "title": title,
            "published": published[:10],
            "bodyText": bodyText,
            'publisher': publisher, 
            # 'instances': instances,
        })


    return years, months, titles, published_dates, bodyTexts

def combine_data():
    for country in COUNTRIES:
        for keyword in keywords:

            years = {country: []} 
            months = {country: []} 
            titles = {country: []} 
            published_dates = {country: []} 
            bodyTexts = {country: []} 


            filenames = os.listdir(os.path.join('data', country))
            for filename in filenames:
                with open(os.path.join('data', country+'/'+filename), 'r') as f:
                    data = json.load(f)
                    years,months, titles, published_dates, bodyTexts = extract_readable_data(country, data, keyword, years, months, titles, published_dates, bodyTexts)

                

            # make the new directory if it doesn't exist
            if not os.path.exists(os.path.join('data', country+'_dates')):
                os.makedirs(os.path.join('data', country+'_dates'))
            with open(os.path.join('data', country+'_dates/'+keyword+'.json'), 'w') as f:
                # save the years months title dates and texts in separate files
                with open(os.path.join('data', country+'_dates/years.json'), 'w') as f:
                    json.dump(years, f)
                with open(os.path.join('data', country+'_dates/months.json'), 'w') as f:
                    json.dump(months, f)
                with open(os.path.join('data', country+'_dates/titles.json'), 'w') as f:
                    json.dump(titles, f)
                with open(os.path.join('data', country+'_dates/published_dates.json'), 'w') as f:
                    json.dump(published_dates, f)
                with open(os.path.join('data', country+'_dates/bodyTexts.json'), 'w') as f:
                    json.dump(bodyTexts, f)



            # Make a new plot per country for the count of years
            for country in years.keys():
                # Convert string years to integers, filter out non-digit/empty entries
                years_int = [int(y) for y in years[country] if str(y).isdigit()]
                if not years_int:
                    continue
                plt.figure()
                plt.hist(years_int, bins=range(min(years_int), max(years_int)+2), edgecolor='black', color='skyblue')
                plt.xlabel('Year')
                plt.ylabel('Count')
                plt.title('Count of Forest Fires Articles by Year in ' + country)
                plt.savefig('summary_stats/forestfire/figs/count_of_forest_fires_by_year_' + country + '.png')
                plt.close()

    
    # plot the count of the months in a histogram per country 
    for country in months.keys():
        plt.figure()
        months_int = [int(m) for m in months[country] if str(m).isdigit()]
        if not months_int:
            continue
        plt.hist(months_int, bins=range(1, 13), color='skyblue', edgecolor='black')
        plt.xlabel('Month')
        plt.ylabel('Count')
        plt.title('Count of Forest Fires Articles by Month in '+country)
        plt.savefig('summary_stats/forestfire/figs/count_of_forest_fires_by_month_'+country+'.png')
        plt.close()

if __name__ == "__main__":
    combine_data()