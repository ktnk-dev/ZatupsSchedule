import flet as ft
from time import sleep
from datetime import datetime

from . import Navigator, NavigatorPage, setup

from config import REPO_URL, VERSION, TIMEOUT

def updater(page: ft.Page):
    def update(e):
        try: page.client_storage.set('date', False)
        except: pass
        page.close(banner)
        
        page.navigation_bar = None
        page.update()
        sleep(.1)
        page.clean()
        sleep(.1)
        setup.login(page, True)
        setup.navigator(page)
        
    banner = ft.AlertDialog(
        modal=False,
        title=ft.Text("Подтверждение"),
        content=ft.Row([
            ft.Text("Во время обновления приложение будет недоступно. Расписание не всегда доступно, имейте ввиду. Это может занять до 2 минут"),
            # ft.Container(height=3),
            ft.Text(f"Последнее обновление {(datetime.now()-datetime.strptime(page.client_storage.get('date'), '%d/%m/%Y, %H:%M:%S')).days} дн. назад", size=13, color=ft.Colors.SECONDARY), #type: ignore | always exist
        ], wrap=True),
        actions=[
            ft.TextButton("Отменить", on_click=lambda _: page.close(banner)),
            ft.FilledButton("Обновить", on_click=lambda _: (page.close(banner), update(None)), bgcolor=ft.Colors.RED),
        ],
        on_dismiss=lambda _: (page.close(banner), page.remove(banner))
    )
    page.add(banner)
    page.open(banner)
    

def settheme(page: ft.Page, target: str | None = 'BLUE'):
    if target: page.client_storage.set('theme', target)
    else: target = page.client_storage.get('theme')
    if not target: target = 'blue'
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors[target.upper()], #type: ignore
        use_material3=True
    )
    
    page.update()
    
def settingspage(page: ft.Page, throw):
    themecolors = [
        ft.Colors.RED,
        # ft.Colors.DEEP_ORANGE,
        ft.Colors.ORANGE,
        # ft.Colors.AMBER,
        ft.Colors.YELLOW,
        # ft.Colors.LIME,
        # ft.Colors.LIGHT_GREEN,
        ft.Colors.GREEN,
        # ft.Colors.TEAL,
        ft.Colors.CYAN,
        ft.Colors.BLUE,
        ft.Colors.INDIGO,
        ft.Colors.PURPLE,
        ft.Colors.PINK,
    ]
    def t(c):
        def h(_): settheme(page, c)
        return h
    
    themechangealert = ft.AlertDialog(
        title='Смена цвета',
        content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.CIRCLE,
                    height=30,
                    width=30,
                    bgcolor=c,
                    icon_color=c,
                    icon_size=0,
                    on_click=t(c)
                ) for c in themecolors
            ], scroll=ft.ScrollMode.AUTO, wrap=True),
        actions=[ft.OutlinedButton('Закрыть', on_click=lambda _: page.close(themechangealert))]
    )
    page.add(themechangealert)
    timeout_switch = ft.Switch(' Автообновление данных', value=not page.client_storage.get('ignore_timeout'), on_change=lambda _: page.client_storage.set('ignore_timeout', not timeout_switch.value))
    throw(ft.Column([
        ft.Text('Тема приложения', size=20),
        ft.FilledButton('Сменить цвет', on_click=lambda _: page.open(themechangealert)),
        ft.Container(height=10),
        ft.Text('Данные', size=20),
        ft.Text(f'Расписание будет актуально {TIMEOUT} дн. после чего произойдет обновление во время запуска приложения'),
        ft.Container(height=0),
        timeout_switch,
        ft.FilledButton('Обновить расписание сейчас', on_click=lambda _: updater(page)),
        ft.Text(f"Последнее обновление {(datetime.now()-datetime.strptime(page.client_storage.get('date'), '%d/%m/%Y, %H:%M:%S')).days} дн. назад", size=13, color=ft.Colors.SECONDARY), #type: ignore | always exist
        ft.Container(height=10),
        ft.Text('Другое', size=20),
        ft.Row([
            ft.FilledButton('Исходный код', on_click=lambda _: page.launch_url(f'{REPO_URL}')),
            ft.FilledButton('Сообщить об ошибке', on_click=lambda _: page.launch_url(f'{REPO_URL}/issues/new')),
        ]),
        ft.Text(f'Версия {VERSION}\nПод лицензией GNU GPL v3', size=13, color=ft.Colors.SECONDARY),
    ]))
    
# {REPO_URL}/issues/new

Navigator.add(
    NavigatorPage(
        label='Настройки',
        icon=ft.Icons.SETTINGS,
        handler=settingspage,
        position=999
    )
)