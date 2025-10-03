'''
2 countries, 1 topic  (Japan, US on climate resilience, climate adaptation) on the first 50 articles (highly relevant ones) 


'''

import os
import json
from collections import Counter
import re


def get_popular_keywords(countries, keywords):
    for country in countries:   
        for keyword in keywords:
            with open(os.path.join('/Users/nicolemeister/Desktop/STANFORD/cultural_defaults/data', country+'_2sentence/'+keyword+'.json'), 'r') as f:
                data = json.load(f)
            
            # Aggregate all instance lists into one large string
            instances = " ".join([" ".join(item["instances"]) for item in data])
            # Process the large string "instances" for the top 20 most popular keywords

            # Tokenize the string into words (simple split, lowercased, remove punctuation)
            # Remove punctuation and make lowercase
            words = re.findall(r'\b\w+\b', instances.lower())

            # Count word frequencies
            word_counts = Counter(words)

            # Get the 20 most common keywords
            top_20 = word_counts.most_common(100)

            print(f"Top 20 keywords for {country} {keyword}:")
            for word, count in top_20:
                print(f"{word}: {count}")

            # save these keywords into a file
            # make the results folder if it doesn't exist
            if not os.path.exists(os.path.join('/Users/nicolemeister/Desktop/STANFORD/cultural_defaults/results')):
                os.makedirs(os.path.join('/Users/nicolemeister/Desktop/STANFORD/cultural_defaults/results'))
            # make the country folder if it doesn't exist
            if not os.path.exists(os.path.join('/Users/nicolemeister/Desktop/STANFORD/cultural_defaults/results', country+'_2sentence')):
                os.makedirs(os.path.join('/Users/nicolemeister/Desktop/STANFORD/cultural_defaults/results', country+'_2sentence'))
            with open(os.path.join('/Users/nicolemeister/Desktop/STANFORD/cultural_defaults/results', country+'_2sentence/'+keyword+'_popular_keywords.txt'), 'w') as f:
                for word, count in top_20:
                    f.write(f"{word}: {count}\n")   
            




if __name__ == "__main__":
    # plot relevance score vs published date
    countries = ["China", "US"]
    keywords = ["%22climate+justice%22", "%22climate+equity%22"]

    get_popular_keywords(countries, keywords)

    # data = get_data("Japan", "%22climate+resilience%22")
    # print(data[:50])