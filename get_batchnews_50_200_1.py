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

# keywords = ["%22climate+equity%22", "%22nature-based+solutions%22", "%22regenerative+agriculture%22", "%22agroforestry%22"]
# keywords = ["%22Australian+Bushfires%22", "%22Typhoon+Hagibis%22", "%22Henan+Floods%22"]
# keywords = ["%22climate+resilience%22", "%22climate+adaptation%22"]
keywords=['%22forest+fire%22']



# keywords = ["%22climate+equity%22", "%22climate+justice%22", "%22nature-based+solutions%22", "%22regenerative+agriculture%22", "%22agroforestry%22", "%22Australian+Bushfires%22", "%22Typhoon+Hagibis%22", "%22Henan+Floods%22", "%22climate+resilience%22", "%22climate+adaptation%22", '%22green+infrastructure%22']


country_to_locationID = {
    "US_wildfires_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NDUxMzNBNDA4QkQwNEVFMEEwMDI0NTc5QkJGMUVBMkI7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAzMDgxMjI3O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjQ1MTMzQTQwOEJEMDRFRTBBMDAyNDU3OUJCRjFFQTJCO2FsdG5hbWU9VVM%27)", 
    "Australia_wildfires_1": "(Location+eq+%27Z3VpZD11cm46a3JtOnB2aS1FRjVERkJDMDhBRDU0RDRFOUEwOThDNTAxOTMwMzFDQjtwYXJlbnRndWlkPQ%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMDA4MjM4O3BhcmVudGd1aWQ9dXJuOmtybTpwdmktRUY1REZCQzA4QUQ1NEQ0RTlBMDk4QzUwMTkzMDMxQ0I7YWx0bmFtZT1BVQ%27)",  
    "Canada_wildfires_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NDUxMzNBNDA4QkQwNEVFMEEwMDI0NTc5QkJGMUVBMkI7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNzMzMjgwO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjQ1MTMzQTQwOEJEMDRFRTBBMDAyNDU3OUJCRjFFQTJCO2FsdG5hbWU9Q0E%27)",
                         }


# country_to_locationID = {
#     "Japan_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNzA4NDcyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9SlA%27)",       
#     "US_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NDUxMzNBNDA4QkQwNEVFMEEwMDI0NTc5QkJGMUVBMkI7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAzMDgxMjI3O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjQ1MTMzQTQwOEJEMDRFRTBBMDAyNDU3OUJCRjFFQTJCO2FsdG5hbWU9VVM%27)", 
#     "SouthKorea_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMDE0NTQxO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9S1I%27)", 
#     "China_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNzY3MjE4O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9Q04%27)",
#     "Singapore_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMTgwMjI1O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9U0c%27)",
#     "Vietnam_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMTc1MDAyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9Vk4%27)",
#     "Germany_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNDE1NjUzO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9REU%27)", 
#     "France_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMDc5NDQyO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9RlI%27)", 
#     "UK_3": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMzE1ODg0O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9R0I%27)", 
#     "Australia_3": "(Location+eq+%27Z3VpZD11cm46a3JtOnB2aS1FRjVERkJDMDhBRDU0RDRFOUEwOThDNTAxOTMwMzFDQjtwYXJlbnRndWlkPQ%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMDA4MjM4O3BhcmVudGd1aWQ9dXJuOmtybTpwdmktRUY1REZCQzA4QUQ1NEQ0RTlBMDk4QzUwMTkzMDMxQ0I7YWx0bmFtZT1BVQ%27)",  
#                          }

# country_to_locationID = {
#     "Norway_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMzg3ODExO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9Tk8%27)",
#     "Bangladesh_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMjg2NjI5O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9QkQ%27)", 
#     "India_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNTMwMjU1O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9SU4%27)",
#     "Malaysia_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNzA1NjIwO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9TVk%27)",
#     "Taiwan_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMzYxNjkxO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9VFc%27)",
#     "Thailand_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwNjUwNDAxO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9VEg%27)",
#     "Nepal_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMDY4NTU5O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9TU4%27)",
#     "Laos_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNzkwMTg0O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9TEE%27)", 
#     "Mongolia_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMDY4NTU5O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9TU4%27)",
#     "SriLanka_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMzA0OTUwO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9TEs%27)",
#     "Phillipines_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06REU0NjQ5QkUzNDNFNDVDMDhCN0JDODZEQ0I3MzRENzg7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwMTYzNzg1O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOkRFNDY0OUJFMzQzRTQ1QzA4QjdCQzg2RENCNzM0RDc4O2FsdG5hbWU9UEg%27)",
#     "Denmark_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAwOTU4NzQwO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9REs%27)",
#     "Canada_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NDUxMzNBNDA4QkQwNEVFMEEwMDI0NTc5QkJGMUVBMkI7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNzMzMjgwO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjQ1MTMzQTQwOEJEMDRFRTBBMDAyNDU3OUJCRjFFQTJCO2FsdG5hbWU9Q0E%27)",
#     "Netherland_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyMTcxNDI5O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9Tkw%27)",
#     "Belgium_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAyNTE5NTQ4O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9QkU%27)",
#     "Switzerland_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMjQxMDUzO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9Q0g%27)",
#     "Spain_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxMTQyMzIzO3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9RVM%27)",
#     "Italy_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNTUzMjQ0O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9SVQ%27)",
#     "Greece_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNTIxMjE2O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9R1I%27)",
#     "Ireland_1": "(Location+eq+%27Z3VpZD11cm46cHJvcGVydHlWYWx1ZUl0ZW06NjMyQUQ2NzIwNzcyNEVBQThGQTRBNDg5N0UxOTUwRDc7cGFyZW50Z3VpZD0%27+and+Location+eq+%27Z3VpZD11cm46ZW50aXR5Omdlb2ItMTAxNzk3MTk0O3BhcmVudGd1aWQ9dXJuOnByb3BlcnR5VmFsdWVJdGVtOjYzMkFENjcyMDc3MjRFQUE4RkE0QTQ4OTdFMTk1MEQ3O2FsdG5hbWU9SUU%27)",
#                          }



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

for i in range(100, 150):
    DOCS_TO_SKIP=i*50

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
                try: data['Document_Content']=result['Document']['Content']
                except: data['Document_Content']=None
                try: data['Document_Citation']=result['Document']['Citation']
                except: data['Document_Citation']=None
                try: data['Source_Name']=result['Source']['Name']
                except: data['Source_Name']=None
                all_data.append(data)

            # save the results 
            with open('data/{}/{}_{}_{}.json'.format(country, keyword, str(total), str(DOCS_TO_SKIP)), 'w') as f:
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
