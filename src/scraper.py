from curl_cffi import requests
from bs4 import BeautifulSoup as bs

#might be used, not sure yet...
state_map = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}
def create_query(strDict) -> bs:
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