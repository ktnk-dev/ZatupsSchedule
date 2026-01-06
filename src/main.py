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
    settings.setthemevariant(page)
    settings.settheme(page, None)
    setup.login(page)
    setup.navigator(page)
    setup.app_update_check(page)
    
ft.app(main)


