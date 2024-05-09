from fastapi import FastAPI

from nicegui import app, ui
from datetime import date as dt
from bs4 import BeautifulSoup as bs

import scraper

#A function is defined here to handle the return value of scraper.create_query
def handle_query(dict):
    #query_result is a soup that we will render shortly
    query_result = scraper.create_query(dict)
    if query_result is None:
        ui.label(text="Nothing found!")
    else:
        query_result = query_result.find('div', {'data-stid': 'property-listing-results'})
        html_string = str(query_result)
        query_result_render = ui.html(html_string).bind_content(html_string)

def init(fastapi_app: FastAPI) -> None:

    @ui.page('/')
    def show():
        ui.label('Enter a location along with the dates you''re looking for')
        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

        with ui.row():
            #Location
            with ui.input('Location', placeholder='Where do you want to go?', 
                        on_change=lambda e: result.set_text(e.value)).add_slot('append'):
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
                    toggle1 = ui.toggle([1,2,3], value=1)
            
            # #Search button
            # ui.button(text="Search", on_click=lambda: scraper.create_query(
            #     {'location':result.text, 'from_date':from_date.text, 'to_date':to_date.text}
            # ))


        ui.button(text="Search", on_click=lambda: handle_query(
            {'location':result.text, 'from_date':from_date.text, 'to_date':to_date.text}
        ))
        result = ui.label()
        from_date = ui.label()
        to_date = ui.label()
        

    ui.run_with(
        fastapi_app,
        mount_path='/gui',
        storage_secret='pick your private secret here',
    )