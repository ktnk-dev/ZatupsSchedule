import flet as ft
from time import sleep
from datetime import datetime

import api
from storage import Storage
from pages import Navigator
from components.spinner import spinner_fulscreen

def login(page: ft.Page):
    Storage.get() #! init
    page.vertical_alignment = ft.MainAxisAlignment.CENTER    
    print(123, page.client_storage.get('date'))
    
    if \
        (
            not page.client_storage.get('date')\
            or (datetime.now() - datetime.strptime(page.client_storage.get('date'), '%d/%m/%Y, %H:%M:%S')).days > api.TIMEOUT \
        ) and not page.client_storage.get('ignore_timeout'): # type: ignore
        
        text = ft.Text('Инициализация...')
        pb = spinner_fulscreen(page, text)
        page.client_storage.set('token', api.authorize())
        
        page.update()
        for progress in api.cache(
            page.client_storage.get('token')
        ):
            pb.value = progress
            text.value = f'Обновление данных... {round(progress*100)}%'
            page.update()
        page.client_storage.set('date', datetime.now().strftime('%d/%m/%Y, %H:%M:%S'))
        sleep(.3)
    
    
def navigator(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.START
    Navigator.build(page)