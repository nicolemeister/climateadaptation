# This boilerplate code has been provided to help you get started with 
# querying LexisNexis. This script assumes you have already already saved
# an api access token as an environment variable. For information on how
# to obtain an access token for the Lexis Nexis API, see get_token.py.
# For information on how to save an environment variable, review this
# repo's README.md.

# Note: Access tokens are only valid for 24 hours. You need to generate a
# new token each day.

# Once executed, this script will print full text resutls from a LexisNexis
# BatchNews query to the screen.

# It is strongly recommended that you read through all notes and
# comments in this boilerplate script to gain an understanding of how
# it works.

# You are welcome to reuse, rewrite, and reformat this boilerplate code
# into your scripts and to add functionality, such as parsing and saving
# results to a file.

import os
import json
from pprint import pprint

import requests
from collections import defaultdict

keywords = ["%22hurricane+katrina%22", "%22climate+justice%22"]
country_to_locationID = {
    # "Japan": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNzA4NDcyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9SlA%27)",       
    # "SouthKorea": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMDE0NTQxO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9S1I%27)", 
    # "China": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNzY3MjE4O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9Q04%27)",
    # "Singapore": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMTgwMjI1O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9U0c%27)",
    # "Vietnam": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMTc1MDAyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9Vk4%27)",
    # "US": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NDUxMzNBNDA4QkQwNEVFMEEwMDI0NTc5QkJGMUVBMkI7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAzMDgxMjI3O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjQ1MTMzQTQwOEJEMDRFRTBBMDAyNDU3OUJCRjFFQTJCO2FsdG5hbWU9VVM%27)", 
    # "Germany": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNDE1NjUzO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9REU%27)", 
    # "France": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMDc5NDQyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9RlI%27)", 
    # "UK": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMzE1ODg0O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9R0I%27)", 
    # "Australia": "(Location+eq+%27Z3VpZD11cm46a3JtOnB2aS1FRjVERkJDMDhBRDU0RDRFOUEwOThDNTAxOTMwMzFDQjtwYXJlbnRndWlkPQ%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMDA4MjM4O3BhcmVudGd1aWQ9dXJuOmtybTpwdmktRUY1REZCQzA4QUQ1NEQ0RTlBMDk4QzUwMTkzMDMxQ0I7YWx0bmFtZT1BVQ%27)",  
    "Norway": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMzg3ODExO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9Tk8%27)"

                        }


# input query string from Web Services User Interface,
# LexisNexis API to query, and API token
# outputs response from
def query(url, token):
    
    headers = {
                'Authorization' : 'Bearer '+token,
                }

    # get request including authentication token in
    # the header and query string
    content = requests.get(url, headers=headers)

    print (content)

    results = content.json()

    return results

NUMBER_OF_DOCS_TO_GRAB = 50
DOCS_TO_SKIP=0

# Read token from environment variables
# see this repo's README.md for instructions on how to set environ variables
token = os.environ["lntoken"]


for country in country_to_locationID.keys():
    os.makedirs('data/{}'.format(country), exist_ok=True)
    for keyword in keywords:
        data_list = []
        locationID = country_to_locationID[country]
        
        url = "https://services-api.lexisnexis.com/v1/News?$expand=Document,PostFilters,Source&$search="+keyword+"&$filter="+locationID+"&$top="+str(NUMBER_OF_DOCS_TO_GRAB)+"&$skip="+str(DOCS_TO_SKIP)

        results = query(url, token)
        total = results['@odata.count']

        # store the value at results['value']
        all_data = []
        for i in range(len(results['value'])): 
            result = results['value'][i]
            data={}
            data['Document_Content']=result['Document']['Content']
            data['Document_Citation']=result['Document']['Citation']
            data['Source_Name']=result['Source']['Name']
            all_data.append(data)

        # save the results 
        with open('data/{}/{}_{}.json'.format(country, keyword, str(total)), 'w') as f:
            json.dump(all_data, f, indent=4)

# # pretty print json results to screen
# pprint(results)

# total = results['@odata.count']
# print("Total number of responses: "+str(total))

# # Getting nextLink to loop through results
# nextLink = results['@odata.nextLink']

# # results['value'] is the dict 

# print(nextLink)
# # you can use this nextLink in the query function, like this
# # next_results = query(nextLink, token)

# breakpoint()

# Example Response
"""

{
    "@odata.context": "https://services-api.lexisnexis.com/v1/$metadata#BatchNews(ResultId,Document,Source)",
    "@odata.count": 3799,
    "@odata.nextLink": "https://services-api.lexisnexis.com/v1/BatchNews?$expand=Document,Source&$filter=Subject%20eq%20'Z3VpZD11cm46dG9waWM6N0FFQjI4MTMyN0RDNDk0NEIyMEYwODA4RTUyODNEQTA7cGFyZW50Z3VpZD0'%20and%20year(Date)%20eq%202008&$select=ResultId&$top=50&$skip=150&$search=inflation+oil",
    "value": [
        {
            "Document": {
                "Citation": "",
                "Content": "...",
                "DocumentId": "/shared/document/news/urn:contentItem:4RHG-MWEL-0MDS1-K0PG-00000-00",
                "DocumentIdType": "DocFullPath",
                "GenAIEnabled": null
            },
            "ResultId": "urn:contentItem:4RHG-MWEL-0MDS1-K0PG-00000-00",
            "Source": {
                "ContentType": "",
                "Id": "",
                "Name": "The Canadian Country Press"
            }
        }
    ]
}

"""

## Notes on Query Parameters

# $top  | used to set the number of results returned. If parameter is not present,
#         it defaults to 10, can be set from 1 up to 50
# $skip | used to skip ahead in the results

# Examples:
# $top=50&$skip=50  | shows results 51-100
# $top=30&$skip=160 | shows results 161-190
# $top=50&$skip=13  | shows results 14-64


## Full Text parameter

# $expand=Document | this parameter will include the full text of each
# item returned in the search results


## Looping through results

# LexisNexis helpfully provides a "nextLink" value that will automatically interate for your top and skip paramters
# See example on line 94
