from collections import Counter
import json


COUNTRIES = ["Canada_wildfires_1", "Australia_wildfires_1", "US_wildfires_1", ]
keywords = ["%22forest+fire%22"]

for country in COUNTRIES:

    # load the labels for this country
    with open(f'data/wildfires_1_labels/{country}_labels.json', 'r') as f:
        labels = json.load(f)


    counts = Counter(x for x in labels if x in ("0", "1"))
    print(country, (counts["0"] + counts["1"]))

    print("0s:", counts["0"]/ (counts["0"] + counts["1"]))
    print("1s:", counts["1"]/ (counts["0"] + counts["1"]))
