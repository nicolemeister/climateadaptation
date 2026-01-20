# combine the data from the different countries into one big file/dictionary 
import os
import json
import re
import random
from utils import model

gpt4o_mini = model.Model(model_name="gpt-4o-mini")

# read promtp from this path: prompts/optimism_realism.txt
with open(os.path.join('prompts', 'themes.txt'), 'r') as f:
    prompt = f.read()



event_name = "Henan Floods"
# read in coding_defaults/optimism_realism/input.json
henan_floods_path = 'data/China_combined/%22Henan+Floods%22.json'
# katrina_path = 'data/US/%22hurricane+katrina%22_312468.json'

with open(henan_floods_path, 'r') as f:
    henan_floods_data = json.load(f)

# make a list of all the things at 'bodyText' in the list of dictionaries 
body_texts = [ex['bodyText'] for ex in henan_floods_data]
results = []
for body_text in body_texts:
  
    body_textprompt = prompt.format(event=event_name) + f"\n\nArticle: {body_text}\nLabel: \n\n"
    model_coding = gpt4o_mini.run_query(body_textprompt)
    results.append({
        "bodytext": body_text,
        "model_coding": model_coding,
    })



# save results to a json file
with open(os.path.join('coding_defaults/themes1_{}.json'.format(event_name)), 'w', encoding='utf-8') as f:
    json.dump(results, f)



event_name = "Hurricane Katrina"
# read in coding_defaults/optimism_realism/input.json
katrina_path = 'data/US/%22hurricane+katrina%22_312468.json'

with open(katrina_path, 'r') as f:
    katrina_data = json.load(f)

# make a list of all the things at 'bodyText' in the list of dictionaries 
body_texts = [ex['Document_Content'] for ex in katrina_data]
results = []
for body_text in body_texts:
  
    body_textprompt = prompt.format(event=event_name) + f"\n\nArticle: {body_text}\nLabel: \n\n"

    model_coding = gpt4o_mini.run_query(body_textprompt)
    results.append({
        "bodytext": body_text,
        "model_coding": model_coding,
    })


# save results to a json file
with open(os.path.join('coding_defaults/themes1_{}.json'.format(event_name)), 'w', encoding='utf-8') as f:
    json.dump(results, f)


