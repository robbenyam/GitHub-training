import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

#Python 2.7.6
#RestfulClient.py

import requests
from requests.auth import HTTPDigestAuth
import json
from pandas.io.json import json_normalize
import athome_common_set as acs
import os

OPATH = acs.OPATH

# Replace with the correct URL
url = ['https://api.sansan.com/v1.2/bizCards/search?range=all',
       'https://api.sansan.com/v1.2/bizCards?registeredFrom="2016-12-01"&registeredTo="2016-12-25"',
       "https://api.sansan.com/v1.2/bizCards/{}",
       "https://api.sansan.com/v1.2/bizCards/{}/image",
       "https://api.sansan.com/v1.2/bizCards/{}/tags",
       "https://api.sansan.com/v1.2/persons/{}",
       "https://api.sansan.com/v1.2/tags"]

# It is a good practice not to hardcode the credentials.
# So ask the user to enter credentials at runtime
headers = {
    'X-Sansan-App-Id': '',
    'X-Sansan-Api-Key': '66866edaab49445b872770ac6ec06662'
}
myResponse = requests.get(url[0],headers = headers)
myResponse1 = requests.get(url[1],headers = headers)
myResponse2 = requests.get(url[2],headers = headers)
myResponse3 = requests.get(url[3],headers = headers)
myResponse4 = requests.get(url[4],headers = headers)
myResponse5 = requests.get(url[5],headers = headers)
myResponse6 = requests.get(url[6],headers = headers)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content.decode('utf-8'))

    print("The response contains {0} properties".format(len(jData)))
    print("\n")
    df = json_normalize(jData['data'])
    print (df)
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()
df.to_csv(os.path.join(OPATH,'test.csv'))