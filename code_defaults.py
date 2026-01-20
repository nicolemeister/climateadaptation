# combine the data from the different countries into one big file/dictionary 
import os
import json
import re
import random
from utils import model

gpt4o_mini = model.Model(model_name="gpt-4o-mini")

# read promtp from this path: prompts/optimism_realism.txt
with open(os.path.join('prompts', 'optimism_realism.txt'), 'r') as f:
    prompt = f.read()

# read in coding_defaults/optimism_realism/input.json
with open(os.path.join('coding_defaults', 'optimism_realism', 'input.json'), 'r') as f:
    data = json.load(f)

# pick 6 random examples from the data to be the few_shot_examples
few_shot_examples = random.sample(data, 11)
few_shot_examples_prompt = ""

for ex in few_shot_examples:
    context = ex['context']
    paragraph = ex['paragraph']
    coding = ex['coding']
    few_shot_examples_prompt += f"Context: {context}\nParagraph: {paragraph}\nCoding: {coding}\n\n"

# pick 6 random examples from the data to be the test_examples that were not used in the few_shot_examples
test_examples = [ex for ex in data if ex not in few_shot_examples]
test_examples = random.sample(test_examples, 1)
results = []
test_examples_prompt = ""
for ex in test_examples:
    context = ex['context']
    paragraph = ex['paragraph']
    coding = ex['coding']
    test_examples_prompt += f"Context: {context}\nParagraph: {paragraph}\nCoding: \n\n"

    prompt = prompt.format(few_shot_examples=few_shot_examples_prompt, test_examples=test_examples_prompt, len_few_shot_examples=len(few_shot_examples))
    model_coding = gpt4o_mini.run_query(prompt)
    results.append({
        "few_shot_examples_prompt": few_shot_examples_prompt,
        "test_examples_prompt": test_examples_prompt,
        "model_coding": model_coding,
        "human_coding": coding
    })

# count the number of times the model coding matches the human coding
num_matches = 0
for result in results:
    if result['model_coding'] == result['human_coding']:
        num_matches += 1
acc = (num_matches / len(results))
results.append({"accuracy": acc})

# save results to a json file
with open(os.path.join('coding_defaults/optimism_realism', '{}_train_{}_test'.format(len(few_shot_examples), len(test_examples)), 'results_{}.json'.format(random.randint(1, 1000000))), 'w', encoding='utf-8') as f:
    json.dump(results, f)
