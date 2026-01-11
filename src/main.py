import flet as ft

from pages import (
    current_schedule,
    search,
    settings,
    setup
)

def main(page: ft.Page):
    page.padding = ft.Padding(10,10,10,0)
    page.title = 'Расписание'
    page.spacing = 0
    # page.client_storage.clear() #! testing

    if not page.client_storage.get('theme_variant'):
        page.client_storage.set('theme_variant', 'auto')
    
    settings.setthemevariant(page)
    settings.settheme(page, None)

    setup.login(page)
    setup.navigator(page)
    setup.app_update_check(page)
    
ft.app(main)


