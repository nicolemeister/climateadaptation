# This boilerplate code has been provided to help you get started with 
# querying LexisNexis. This script assumes you have already saved your client
# id and client secret as environment variables.  Review this repo's README.md
# for information on how to do this.

# Once executed, this script will save the newly generated token as a
# environment variable, however this token is not available after the
# script completes. This script is only provided as an example of how
# to generate an access token from credentials.

# It is strongly recommended that you read through all notes and
# comments in this boilerplate script to gain an understanding of how
# it works.

# You are welcome to reuse, rewrite, and reformat this boilerplate code
# into your scripts.

import os
import json

import requests
from requests.auth import HTTPBasicAuth

# This function retrieves a Lexis Nexis API access token.
# inputs:  clientid and secret
# outputs: response from LexisNexis Authentication API which includes
#          an API token valid for 24 hours
# uses BaicAuthentication
def get_token(clientid, clientsecret):

    basic = HTTPBasicAuth(clientid, clientsecret)
    
    url = "https://auth-api.lexisnexis.com/oauth/v2/token"
    data = "grant_type=client_credentials&scope=http%3a%2f%2foauth.lexisnexis.com%2fall"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    # post request including required headers, data, and basic authenticaation
    response = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(clientid, clientsecret))

    results = response.json()

    return results

# Read credentials from environment variables
# See this repo's README.md for instructions on how to set environ variables.
clientid = os.environ["clientid"]
clientsecret = os.environ["clientsecret"]

# execute get_token function using the client id and secret
token_data = get_token(clientid, clientsecret)

# print full response from LexisNexis Authentication API
print(token_data)

# isolate the token from the full response
token = token_data["access_token"]

# Save token as environment variable for this session, the
# token will not be available after this script completes.
# To use this token outside of this script set the token
# manually set it ias an environment variable. See this repo's
# README.md for instructions on how to set environ variables.
os.environ['lntoken'] = token

# print just the 24 hour token to screen
print(token)