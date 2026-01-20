import os
import json
from utils.model import Model


with open('/nlp/scr/nmeist/climateadaptation/data/Australia_wildfires_1_dates/bodyTexts.json', 'r') as f:
    bodyTexts = json.load(f)

# COUNTRIES = ["Canada_wildfires_1", "Australia_wildfires_1", "US_wildfires_1", ]
COUNTRIES = [  "Australia_wildfires_1",]
keywords = ["%22forest+fire%22"]

model = Model(model_name="gpt-5-nano-2025-08-07")


def is_fire_prevention_discusssed(combined_docs):
    user_prompt_path = "prompts/fire_prevention.txt"
    system_prompt =  "You are a helpful assistant that categorizes news articles about wildfires into two categories: 1 if the article contains discussion of prescribed burning, 0 if it does not contain discussion of prescribed burning."
    response = model.run_query(user_prompt_path, system_prompt, combined_docs)
    return response

# def get_topics(combined_docs):

for country in COUNTRIES:
    # Gather all body texts for this country and split them into 400k token chunks,
    # but don't split any single document across chunks.
    chunks = []
    current_chunk = []
    current_chunk_token_count = 0
    MAX_TOKENS = 10000

    # Function to approximate token count for a text
    def get_token_count(text):
        return int(len(text.split()) / 75 * 100)

    for bodyText in bodyTexts[country]:
        doc_tokens = get_token_count(bodyText)
        # If adding this doc would exceed the chunk size, start a new chunk
        if current_chunk_token_count + doc_tokens > MAX_TOKENS:
            if current_chunk:  # Save previous chunk if not empty
                chunks.append(current_chunk)
            current_chunk = [bodyText]
            current_chunk_token_count = doc_tokens
        else:
            current_chunk.append(bodyText)
            current_chunk_token_count += doc_tokens

    if current_chunk:
        chunks.append(current_chunk)

    print(f"Number of chunks for {country}: {len(chunks)}")

    # for each chunk, combine the documents into a single string
    labels = []
    for chunk in chunks:
        combined_docs = ""
        for idx, doc in enumerate(chunk, 1):
            combined_docs += f"Doc {idx}: {doc}\n\n"
        
        print(combined_docs)
        break
        # # input this combined_docs into the LLM to get the topic model
        # chunk_labels = is_fire_prevention_discusssed(combined_docs) 
        # # convert the string of 0s and 1s into a list of 0s and 1s
        # # labels = [int(label) for label in chunk_labels]
        # print(chunk_labels)
        # labels.extend(chunk_labels)

        #     # save the labels to a json file
        # with open(f'data/wildfires_1_labels/{country}_labels.json', 'w') as f:
        #     json.dump(labels, f)

    # # input combined docs to get a output of how often prevention is discussed 
    # prevention_count = sum(labels)
    # total_count = len(labels)
    # prevention_percentage = prevention_count / total_count
    # print(f"Prevention percentage for {country}: {prevention_percentage}")
