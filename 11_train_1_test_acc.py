# read through all the data in climateadaptation/coding_defaults/optimism_realism/11_train_1_test and calculate the total accuracy
import os
import json

total_accuracy = 0
# read through all the data in climateadaptation/coding_defaults/optimism_realism/11_train_1_test
for file in os.listdir(os.path.join('coding_defaults', 'optimism_realism', '11_train_1_test')):
    with open(os.path.join('coding_defaults', 'optimism_realism', '11_train_1_test', file), 'r') as f:
        data = json.load(f)

    total_accuracy += data[-1]['accuracy']

print(total_accuracy / len(os.listdir(os.path.join('coding_defaults', 'optimism_realism', '11_train_1_test'))))
