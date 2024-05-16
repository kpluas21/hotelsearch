from curl_cffi import requests
from playwright.async_api import async_playwright, Playwright
import time

#a typical url string for an expedia search looks something like this :
#https://www.expedia.com/Hotel-Search?destination=Miami%20%28and%20vicinity%29%2C%20Florida%2C%20United%20States%20of%20America
#&regionId=178286&latLong=25.77178%2C-80.19009&flexibility=0_DAY&d1=2024-05-15&startDate=2024-05-15&d2=2024-05-17&endDate=2024-05-17
#&adults=1%2C1&rooms=2&sort=RECOMMENDED&useRewards=false&semdtl=&userIntent=&theme=

async def create_query(strDict):
    print("Attempting to create a query with the values: ")
    for key in strDict.keys():
        print(f"{key}: {strDict[key]}")

    date_range = ""
    if strDict['location'] != "":
        strDict['location'] = "destination=" + strDict['location']
        strDict['location'] = str(strDict['location']).replace(',', ' (and vicinity)%2C')
        strDict['location'] = strDict['location'] + ('%2C United States of America')
    if strDict['from_date'] and strDict['to_date'] != "":
        date_range = f"&d1={strDict['from_date']}&startDate={strDict['from_date']}&d2={strDict['to_date']}&endDate={strDict['to_date']}"
    if strDict['num_adults'] != "":
        strDict['num_adults'] = f"&adults={str(strDict['num_adults'])}"
    if strDict['num_kids'] != "":
        strDict['num_kids'] = f"&children={str(strDict['num_kids'])}"
    if strDict['num_rooms'] != "":
        strDict['num_rooms'] = f"&rooms={str(strDict['num_rooms'])}"

        
    # print(strDict['location'])
    # print(date_range)

    query = strDict['location'] + date_range + strDict['num_adults'] + strDict['num_kids'] + strDict['num_rooms'] + "&sort=RECOMMENDED&useRewards=false&semdtl=&userIntent=&theme=&allowPreAppliedFilters=false&mapBounds=&pwaDialog="
    print(f"Searching for hotels with query {query}")
    results = await search(query)
    return results

#returns the beautifulSoup object for the frontend to render into a list
async def search(query):
    url = f"https://www.expedia.com/Hotel-Search?{query}"
    print(f"Attempting to request URL: {url}")
    hotels = []

    async with async_playwright() as p:
        browser = await p.firefox.launch(
        )
        page = await browser.new_page()
        await page.goto(url)
        time.sleep(4)
        # show_more = page.locator("button", has_text="Show More")

        # # while await show_more.is_visible() is True:
        # #     await show_more.click()
        # #     time.sleep(5)

        # for i in range(5):
        #     await show_more.click()
        #     time.sleep(5)

        results = await page.locator('[data-stid="lodging-card-responsive"]').all()

        listings = []
        for hotel in results:
            if await hotel.is_visible():
                listings.append(hotel)

        if len(listings) == 0:
            await browser.close()
            return None
        else:
            print(f"{len(listings)} listings found!")
            for listing in listings:
                content =  listing.locator('div.uitk-card-content-section')
                
                #Hotel name
                title = await content.locator('h3').text_content()

                #Price
                if await content.locator('div.uitk-type-500').is_visible():
                    price = await content.locator('div.uitk-type-500').text_content()
                else:
                    print(f"No price found for {title}")
                    price = None

                #Rating
                if await content.locator('span.uitk-badge-base-text').is_visible():
                    rating = await content.locator('span.uitk-badge-base-text').text_content()
                else:
                    print(f"No rating found for {title}")
                    rating = None
                
                #Images
                images = []
                images_locator = await listing.locator('img.uitk-image-media').all()
                print(f"{len(images_locator)} images located for {title}")
                for img in images_locator:
                    if await img.is_visible():
                        images.append(await img.get_attribute('src'))
                    

                hotel = {
                    'title':title,
                    'price':price,
                    'rating':rating,
                    'images':images
                }

                hotels.append(hotel)
            
            await browser.close()
            print("Scraping complete!")
            return hotels
    # response = requests.get(url, impersonate="chrome")

    # if response.ok:
    #     #successful request

    #     #now we parse the actual HTML
    #     soup = bs(response.text, "html.parser")

    #     print("Request successfully sent!")

    #     # print(soup.prettify()) 

    #     #mmmm soup :)
    #     return soup   
    
    # else:
    #     print("Request not sent successfully :(")
    #     print(response.status_code)
    #     print(response.content)
    #     return None
