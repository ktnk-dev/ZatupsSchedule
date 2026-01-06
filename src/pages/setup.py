import flet as ft
from time import sleep
from datetime import datetime

import api
from storage import Storage
from pages import Navigator
from components.spinner import spinner_fulscreen

from config import REPO_URL

def app_update_check(page: ft.Page):
    try:
        required, text = api.app_update_required()
        if not required: return
    except: return 
    def action(update: bool = False):
        def h(_):
            page.close(banner)
            if update: page.launch_url(REPO_URL+'/releases/latest')
        return h
    
    banner = ft.Banner(
        # bgcolor=ft.Colors.SECONDARY_CONTAINER,
        leading=ft.Icon(ft.Icons.UPDATE, color=ft.Colors.SECONDARY),
        content=ft.Text(f'Доступно новое{" критическое" if "critical" in text else ""} обновление', color=ft.Colors.SECONDARY, size=15),
        actions=[
            ft.TextButton("Закрыть", on_click=action()),
            ft.OutlinedButton("Обновить", on_click=action(True)),
        ]
    )
    
    page.add(banner)
    page.open(banner)


def login(page: ft.Page, force_update_condition: bool = False):
    Storage.get() #! init
    page.vertical_alignment = ft.MainAxisAlignment.CENTER    
    # print(123, page.client_storage.get('date'))
    
    incorrect_date_condition = not page.client_storage.get('date')
    timeout_condition = incorrect_date_condition or (datetime.now() - datetime.strptime(page.client_storage.get('date'), '%d/%m/%Y, %H:%M:%S')).days > api.TIMEOUT # type: ignore | unreachable
    allowed_autoupdate_condition = not page.client_storage.get('ignore_timeout')
    
    def setdate():
        page.client_storage.set('date', datetime.now().strftime('%d/%m/%Y, %H:%M:%S'))
    
    if 0 \
        or force_update_condition \
        or incorrect_date_condition \
        or (allowed_autoupdate_condition and timeout_condition) \
    : 
        text = ft.Text('Инициализация...')
        pb = spinner_fulscreen(page, text)
        page.update()
        sleep(1)
        if pb.value == 100: return setdate()

        page.client_storage.set('token', api.authorize())
        
        page.update()
        for progress in api.cache(
            page.client_storage.get('token') # type: ignore | always exists
        ):
            if pb.value == 100: return setdate()
            pb.value = progress
            text.value = f'Обновление данных... {round(progress*100)}%'
            page.update()
        setdate()
        sleep(.3)
    
    
def navigator(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.START
    Navigator.build(page)