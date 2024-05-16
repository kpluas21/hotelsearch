from fastapi import FastAPI

from nicegui import app, ui
from datetime import date as dt

import scraper

# hotel = {
#     'title':title,
#     'price':price,
#     'rating':rating
# }
#A function is defined here to handle the return value of scraper.create_query
async def handle_query(dict):
    #query_result is a soup that we will render shortly
    listings = await scraper.create_query(dict)
    if listings is None:
        ui.label(text="Nothing found!")
    else:
        print("Rendering hotels onto NiceGUI")
        for hotel in listings:
            with ui.column():
                with ui.card():
                    ui.label(hotel['title'])
                    ui.label(hotel['price'] or "NO PRICE")
                    ui.label(hotel['rating'] or "NO RATING")
                    with ui.row():
                        for image in hotel['images']:
                            ui.image(image)
                    # ui.image(source=hotel['image'])
        print("Rendering complete!")
                
                

def init(fastapi_app: FastAPI) -> None:
    search_results = []
    @ui.page('/')
    def show():
        ui.label("Enter a location along with the dates you're looking for")
        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

        with ui.card():
            with ui.row():
                #Location
                with ui.input('Location', placeholder='Where do you want to go?', 
                            on_change=lambda e: location.set_text(e.value)).add_slot('append'):
                    ui.icon('room')
                #From date
                with ui.input('From') as date:
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu1.open()).classes('cursor-pointer')
                    with ui.menu() as menu1:
                        ui.date(value= dt.today(), 
                                on_change=lambda e: from_date.set_text(e.value)).bind_value(date)
                #To date
                with ui.input('To') as date:
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu2.open()).classes('cursor-pointer')
                    with ui.menu() as menu2:
                        ui.date(value=dt.today(), 
                                on_change=lambda e: to_date.set_text(e.value)).bind_value(date)
                
                #Passengers
                with ui.input('Passengers') as people:
                    with people.add_slot('append'):
                        ui.icon('account_circle').on('click', lambda: passenger_select.open()).classes('cursor-pointer')
                    with ui.menu() as passenger_select:
                        ui.label("Adults")
                        num_adults_toggle = ui.toggle([1,2,3,4,5,6], value=2)
                        ui.label("Kids")
                        num_kids_toggle = ui.toggle([0,1,2,3,4,5,6], value=0)
                        ui.label("Rooms")
                        num_rooms_toggle = ui.toggle([1,2,3,4], value=1)

                location = ui.label()
                from_date = ui.label()
                to_date = ui.label()
            ui.button(text="Search", on_click=lambda: handle_query(
                {'location':location.text, 
                'from_date':from_date.text, 
                'to_date':to_date.text, 
                'num_adults': num_adults_toggle.value,
                'num_kids': num_kids_toggle.value,
                'num_rooms': num_rooms_toggle.value}
            )) 

    ui.run_with(
        fastapi_app,
        mount_path='/gui',
        storage_secret='pick your private secret here',
    )