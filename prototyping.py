'''
2 countries, 1 topic  (Japan, US on climate resilience, climate adaptation) on the first 50 articles (highly relevant ones) 


'''

import os
import json
import matplotlib.pyplot as plt
from gensim import corpora, models
from gensim.utils import simple_preprocess
from datetime import datetime


# COUNTRIES = ["Japan", "US", "SouthKorea", "China", "Singapore", "Vietnam", "Germany", "France", "UK", "Australia", "Norway", "Bangladesh", "India", "Malaysia", "Taiwan", "Thailand", "Nepal", "Laos", "Mongolia", "SriLanka", "Phillipines", "Denmark", "Canada", "Netherland", "Belgium", "Switzerland", "Spain", "Italy", "Greece", "Ireland"]
# keywords = ["%22climate+equity%22", "%22climate+justice%22", "%22nature-based+solutions%22", "%22regenerative+agriculture%22", "%22agroforestry%22", "%22Australian+Bushfires%22", "%22Typhoon+Hagibis%22", "%22Henan+Floods%22", "%22climate+resilience%22", "%22climate+adaptation%22", '%22green+infrastructure%22']


def get_topics(texts):

    # Tokenize
    processed_texts = [simple_preprocess(doc) for doc in texts]

    # Build dictionary and corpus
    dictionary = corpora.Dictionary(processed_texts)
    corpus = [dictionary.doc2bow(text) for text in processed_texts]

    # Train LDA
    lda = models.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=10)

    # Assign topics to each document
    doc_topics = lda.get_document_topics(corpus)

    # Show results
    # store this printed text in a text document
    with open(os.path.join('plots', f"topics.txt"), 'w') as f:
        for i, topics in enumerate(doc_topics):
            # topics is a list of (topic_id, prob)
            main_topic = max(topics, key=lambda x: x[1])  # choose highest probability
            f.write(f"Doc {i}: '{texts[i]}'\n")
            f.write(f"   Main Topic: {main_topic[0]} (prob={main_topic[1]:.3f})\n")
            f.write(f"   All Topics: {topics}\n")




def get_data(country, keyword):
    with open(os.path.join('data', country+'_combined/'+keyword+'.json'), 'r') as f:
        data = json.load(f)

    # plot relevance score vs published date
    relevance_scores = [item["relevance_score"] for item in data]
    published_dates = [item["published"] for item in data]
    plt.scatter(relevance_scores, published_dates)
    plt.xlabel("Relevance Score")
    plt.ylabel("Published Date")
    plt.show()

    # combine all the data that is in the "bodyText" keyword into a list of text strings
    text_strings = [item["bodyText"] for item in data]
    get_topics(text_strings)


    # combine all the 
    return data



def plot_relevance_score_vs_published_date(countries, keywords):
    for country in countries:   
        for keyword in keywords:
            with open(os.path.join('data', country+'_combined/'+keyword+'.json'), 'r') as f:
                data = json.load(f)

            # plot relevance score vs published date
            relevance_scores = [item["relevance_score"] for item in data]
            published_dates = [item["published"] for item in data]
            #  for each date in the format "2023-09-20", convert it to a datetime object so that it can be a continuous value
            published_dates = [datetime.strptime(date, "%Y-%m-%d") for date in published_dates]
            
            plt.scatter(relevance_scores, published_dates, 
                        label=f"{country} {keyword}", alpha=0.5)
            plt.xlabel("Relevance Score")
            plt.ylabel("Published Date")

    plt.legend()
    plt.show()
    plt.savefig(os.path.join('plots', f"relevance_score_vs_published_date.png"))



if __name__ == "__main__":
    # plot relevance score vs published date
    countries = ["Japan", "US"]
    keywords = ["%22climate+resilience%22", "%22climate+adaptation%22"]

    plot_relevance_score_vs_published_date(countries, keywords)

    # data = get_data("Japan", "%22climate+resilience%22")
    # print(data[:50])