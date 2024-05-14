from curl_cffi import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
#a typical url string for an expedia search looks something like this :
#https://www.expedia.com/Hotel-Search?destination=Miami%20%28and%20vicinity%29%2C%20Florida%2C%20United%20States%20of%20America
#&regionId=178286&latLong=25.77178%2C-80.19009&flexibility=0_DAY&d1=2024-05-15&startDate=2024-05-15&d2=2024-05-17&endDate=2024-05-17
#&adults=1%2C1&rooms=2&sort=RECOMMENDED&useRewards=false&semdtl=&userIntent=&theme=

def create_query(strDict) -> bs:
    print("Attempting to create a query with the values: ")
    for key in strDict.keys():
        print(f"{key}: {strDict[key]}")

    date_range = ""
    pattern = r'([A-Za-z\s]+),\s*([A-Z]{2})'
    if strDict['location'] != "":
        strDict['location'] = "destination=" + strDict['location']
        strDict['location'] = str(strDict['location']).replace(" ", "")
        strDict['location'] = str(strDict['location']).replace(',', '%2C')
    if strDict['from_date'] and strDict['to_date'] != "":
        date_range = f"&d1={strDict['from_date']}&startDate={strDict['from_date']}&d2={strDict['to_date']}&endDate={strDict['to_date']}"
    # print(strDict['location'])
    # print(date_range)

    query = strDict['location'] + date_range + "&sort=RECOMMENDED"
    print(f"Searching for hotels with query {query}")
    return search(query)

#returns the beautifulSoup object for the frontend to render into a list
def search(query) -> bs:
    url = f"https://www.expedia.com/Hotel-Search?{query}"
    print(f"Attempting to request URL: {url}")

    response = requests.get(url, impersonate="chrome")

    if response.ok:
        #successful request

        #now we parse the actual HTML
        soup = bs(response.text, "html.parser")

        print("Request successfully sent!")

        # print(soup.prettify()) 

        #mmmm soup :)
        return soup   
    
    else:
        print("Request not sent successfully :(")
        print(response.status_code)
        print(response.content)
        return None
