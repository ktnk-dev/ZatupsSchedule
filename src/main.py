import flet as ft

from pages import (
    current_schedule,
    search,
    settings,
    setup
)
import logger
DEBUG = False

def main(page: ft.Page):
    logger.log('main', 'Приложение запущено')
    # page.padding = ft.Padding(10,10,10,0)
    page.title = 'Расписание'
    page.spacing = 0
    # page.client_storage.clear() #! testing

    if DEBUG:
        logger.log('main', 'Добавление кнопки логов...')
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.CODE,
            bgcolor=ft.Colors.RED,
            on_click=lambda _: logger.display(page)
        )
    
    logger.log('main', 'Инициализация темы...')
    if not page.client_storage.get('theme_variant'):
        page.client_storage.set('theme_variant', 'auto')
    

    logger.log('main', 'Запуск "settings.setthemevariant"...')
    settings.setthemevariant(page)
    logger.log('main', 'Запуск "settings.settheme"...')
    settings.settheme(page, None)

    logger.log('main', 'Запуск "setup.login"...')
    setup.login(page)
    logger.log('main', 'Запуск "setup.navigator"...')
    setup.navigator(page)
    logger.log('main', 'Запуск "setup.app_update_check"...')
    setup.app_update_check(page)
    
ft.app(main)
