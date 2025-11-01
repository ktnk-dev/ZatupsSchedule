import flet as ft

from pages import (
    current_schedule,
    search,
    settings,
    setup
)

def main(page: ft.Page):
    page.title = 'Расписание'
    page.spacing = 0
    settings.settheme(page, None)
    setup.login(page, True)
    setup.navigator(page)
    
ft.app(main)


