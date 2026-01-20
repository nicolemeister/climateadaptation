import os
import json
from collections import Counter
import re


# keywords = ["%22hurricane+katrina%22", "%22climate+justice%22", "%22climate+equity%22", "%22nature-based+solutions%22", "%22regenerative+agriculture%22", "%22agroforestry%22", "%22Australian+Bushfires%22", "%22Typhoon+Hagibis%22", "%22Henan+Floods%22"]
keywords = ["%22forest+fire%22"]

keyword_to_searchable_keyword = {
    "%22forest+fire%22": "forest fire"
}
# keyword_to_searchable_keyword = {
#     "%22hurricane+katrina%22": "hurricane katrina",
#     "%22climate+justice%22": "climate justice",
#     "%22climate+equity%22": "climate equity",
#     "%22nature-based+solutions%22": "nature-based solutions",
#     "%22regenerative+agriculture%22": "regenerative agriculture",
#     "%22agroforestry%22": "agroforestry",
#     "%22Australian+Bushfires%22": "Australian Bushfires",
#     "%22Typhoon+Hagibis%22": "Typhoon Hagibis",
#     "%22Henan+Floods%22": "Henan Floods"
# }

country_to_locationID = {
    'US_wildfires': '(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NDUxMzNBNDA4QkQwNEVFMEEwMDI0NTc5QkJGMUVBMkI7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAzMDgxMjI3O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjQ1MTMzQTQwOEJEMDRFRTBBMDAyNDU3OUJCRjFFQTJCO2FsdG5hbWU9VVM%27)',
    "Australia_wildfires": "(Location+eq+%27Z3VpZD11cm46a3JtOnB2aS1FRjVERkJDMDhBRDU0RDRFOUEwOThDNTAxOTMwMzFDQjtwYXJlbnRndWlkPQ%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMDA4MjM4O3BhcmVudGd1aWQ9dXJuOmtybTpwdmktRUY1REZCQzA4QUQ1NEQ0RTlBMDk4QzUwMTkzMDMxQ0I7YWx0bmFtZT1BVQ%27)",  
}

# country_to_locationID = {
#     "Japan": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNzA4NDcyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9SlA%27)",       
#     "SouthKorea": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMDE0NTQxO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9S1I%27)", 
#     "China": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNzY3MjE4O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9Q04%27)",
#     "Singapore": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMTgwMjI1O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9U0c%27)",
#     "Vietnam": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMTc1MDAyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9Vk4%27)",
#     "US": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NDUxMzNBNDA4QkQwNEVFMEEwMDI0NTc5QkJGMUVBMkI7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAzMDgxMjI3O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjQ1MTMzQTQwOEJEMDRFRTBBMDAyNDU3OUJCRjFFQTJCO2FsdG5hbWU9VVM%27)", 
#     "Germany": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNDE1NjUzO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9REU%27)", 
#     "France": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMDc5NDQyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9RlI%27)", 
#     "UK": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMzE1ODg0O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9R0I%27)", 
#     "Australia": "(Location+eq+%27Z3VpZD11cm46a3JtOnB2aS1FRjVERkJDMDhBRDU0RDRFOUEwOThDNTAxOTMwMzFDQjtwYXJlbnRndWlkPQ%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMDA4MjM4O3BhcmVudGd1aWQ9dXJuOmtybTpwdmktRUY1REZCQzA4QUQ1NEQ0RTlBMDk4QzUwMTkzMDMxQ0I7YWx0bmFtZT1BVQ%27)",  
#     "Norway": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMzg3ODExO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9Tk8%27)"
# }

# Read token from environment variables
# See this repo's README.md for instructions on how to set environ variables

output_lines_sourcefreq = []
output_lines_keywordfreq = []
output_lines_keywordcontext = []
output_lines_titles = []
for country in country_to_locationID.keys():
    json_files = [f for f in os.listdir('data/{}/'.format(country)) if f.endswith('.json')]
    for json_file in json_files:
        with open('data/{}/{}'.format(country, json_file), 'r') as f:
            data = json.load(f)

        # Gather all source names
        source_names = [item.get('Source_Name', None) for item in data if 'Source_Name' in item]
        source_counter = Counter(source_names)
        output_lines_sourcefreq.append(f"Summary for {country} - {json_file}:")
        for source, count in source_counter.items():
            output_lines_sourcefreq.append(f"  {source}: {count}")
        output_lines_sourcefreq.append("-" * 40)
        output_lines_keywordcontext.append("-" * 40)
        output_lines_keywordcontext.append(f"Keyword context for {country} - {json_file}:")

        # Extract titles from Document_Content
        titles = []
        keyword_freqs = []
        # Determine which keyword is in this file
        keyword = None
        for k in keywords:
            if k in json_file:
                keyword = k
                break
        search_word = keyword_to_searchable_keyword[keyword] if keyword else None

        for item in data:
            content = item.get('Document_Content', '')
            if content:
                match = re.search(r'<title>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    titles.append(title)
                    if search_word:
                        # Count occurrences of the keyword (case-insensitive, as a phrase)
                        count = len(re.findall(re.escape(search_word), content, re.IGNORECASE))
                        keyword_freqs.append((title, count))

                        # --- Surrounding context extraction (more than previous and next sentence) ---
                        # Remove HTML tags for context extraction
                        content_text = re.sub(r'<.*?>', '', content)
                        # Split into sentences (simple split on . ! ?)
                        import re
                        sentence_splitter = re.compile(r'(?<=[.!?])\s+')
                        sentences = sentence_splitter.split(content_text)
                        # Find all indices where the keyword appears (case-insensitive, as a phrase)
                        keyword_pattern = re.compile(re.escape(search_word), re.IGNORECASE)
                        context_snippets = []
                        for idx, sent in enumerate(sentences):
                            if keyword_pattern.search(sent):
                                # Get two previous and two next sentences if available
                                prev2_sent = sentences[idx-2].strip() if idx > 1 else ""
                                prev1_sent = sentences[idx-1].strip() if idx > 0 else ""
                                next1_sent = sentences[idx+1].strip() if idx < len(sentences)-1 else ""
                                next2_sent = sentences[idx+2].strip() if idx < len(sentences)-2 else ""
                                snippet_parts = []
                                if prev2_sent:
                                    snippet_parts.append(prev2_sent)
                                if prev1_sent:
                                    snippet_parts.append(prev1_sent)
                                snippet_parts.append(sent.strip())
                                if next1_sent:
                                    snippet_parts.append(next1_sent)
                                if next2_sent:
                                    snippet_parts.append(next2_sent)
                                snippet = " ".join(snippet_parts)
                                context_snippets.append(snippet.strip())
                        # Output: title, count, and for each instance, the context snippet
                        output_lines_keywordcontext.append(f"{title} [{count}]")
                        for i, snippet in enumerate(context_snippets, 1):
                            output_lines_keywordcontext.append(f"  Instance {i}: {snippet}")
                        if not context_snippets:
                            output_lines_keywordcontext.append("  No context found.")
                    else:
                        keyword_freqs.append((title, 0))
        output_lines_titles.append(f"Titles for {country} - {json_file}:")
        for title in titles:
            output_lines_titles.append(f"  {title}")
        output_lines_titles.append("-" * 40)

        # Output keyword frequency next to title
        if search_word:
            output_lines_keywordfreq.append(f"Keyword frequency for {country} - {json_file}:")
            for title, freq in keyword_freqs:
                output_lines_keywordfreq.append(f"  {title} [{freq}]")
            output_lines_keywordfreq.append("-" * 40)

with open("summary_stats/forestfire/sources_frequency.txt", "w") as out_f:
    for line in output_lines_sourcefreq:
        out_f.write(line + "\n")

with open("summary_stats/forestfire/titles.txt", "w") as out_f:
    for line in output_lines_titles:
        out_f.write(line + "\n")


with open("summary_stats/forestfire/title_keyword_freq.txt", "w") as out_f:
    for line in output_lines_keywordfreq:
        out_f.write(line + "\n")

with open("summary_stats/forestfire/title_keyword_context.txt", "w") as out_f:
    for line in output_lines_keywordcontext:
        out_f.write(line + "\n")