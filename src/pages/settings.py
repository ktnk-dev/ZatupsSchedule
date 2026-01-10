import flet as ft
from time import sleep
from datetime import datetime

from . import Navigator, NavigatorPage, setup

from config import REPO_URL, VERSION, TIMEOUT
from components.settingsrow import Settings, SettingsTitle, SettingsContainer

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

def setthemevariant(page: ft.Page, target: str | None = None):
    if target: page.client_storage.set('theme_variant', target)
    else: target = page.client_storage.get('theme_variant')
    variants = {
        'light': ft.ThemeMode.LIGHT,
        'dark': ft.ThemeMode.DARK,
        'auto': ft.ThemeMode.SYSTEM
    }
    page.theme_mode = variants.get(target.lower(), ft.ThemeMode.SYSTEM) #type: ignore
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
    def t(c, fn):
        def h(_): fn(page, c)
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
                    on_click=t(c, settheme)
                ) for c in themecolors
            ], scroll=ft.ScrollMode.AUTO, wrap=True),
        actions=[ft.OutlinedButton('Закрыть', on_click=lambda _: page.close(themechangealert))]
    )
    page.add(themechangealert)
    timeout_switch = ft.Switch(
#         ' Автообновление данных', 
        value=not page.client_storage.get('ignore_timeout'), 
        on_change=lambda _: page.client_storage.set('ignore_timeout', not timeout_switch.value)
    )
    def timeout_switch_action(e):
        timeout_switch.value = not timeout_switch.value
        page.client_storage.set('ignore_timeout', not timeout_switch.value)
        page.update()

    themevariantchangealert = ft.AlertDialog(
        title='Смена темы',
        content=ft.Row([
                ft.FilledButton(
                    f'  {text}  ',
                    on_click=t(id, setthemevariant)
                ) for id, text in ({
                    'auto': 'Системная',
                    'light': 'Светлая',
                    'dark': 'Темная',
                }).items()
            ], scroll=ft.ScrollMode.AUTO, expand=True),
        actions=[ft.OutlinedButton('Закрыть', on_click=lambda _: page.close(themevariantchangealert))]
    )
    page.add(themevariantchangealert)

    

    themedropdown = ft.Dropdown(
        text_align=ft.TextAlign.RIGHT,
        border=ft.InputBorder.NONE,
        #expand=True,
        #filled=True,
        #fill_color=ft.Colors.SECONDARY_CONTAINER,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        border_radius=999,
        options=[
            ft.DropdownOption('auto', 'Системная тема'),
            ft.DropdownOption('light', 'Светлая тема'),
            ft.DropdownOption('dark', 'Темная тема'),
            
        ],
        on_change=lambda e: setthemevariant(page, e.control.value), 
        value=page.client_storage.get('theme_variant')
    )

    throw(ft.Column([
        ft.Container(
            ft.Text('Настройки', size=25),
            padding=ft.Padding(5,5,5,0)
        ),
        SettingsTitle('Кастомизация'),
        *SettingsContainer(
            Settings(
                'Сменить тему',
                'Выбери темную или светлую сторону',
                leading=ft.Icon(ft.Icons.PALETTE),
                item=themedropdown,
                on_click=None
            ),
            Settings(
                'Сменить цвет',
                'Цвет темы приложения',
                leading=ft.Icon(ft.Icons.COLORIZE),
                on_click=lambda _: page.open(themechangealert)
            ),
        ),
        SettingsTitle('Расписание'), 
        *SettingsContainer(
            Settings(
                'Автообновление расписания',
                f'Расписание обновляется раз в {TIMEOUT} дн.',
                leading=ft.Icon(ft.Icons.UPDATE),
                item=timeout_switch,
                on_click=timeout_switch_action
            ),
            Settings(
                'Обновить сейчас',
                f"Обновление было {(datetime.now()-datetime.strptime(page.client_storage.get('date'), '%d/%m/%Y, %H:%M:%S')).days} дн. назад", 
                leading=ft.Icon(ft.Icons.DOWNLOAD),
                on_click=lambda _: updater(page)
            ),
        ),
        SettingsTitle('Другое'),
        *SettingsContainer(
            Settings(
                'Открыть исходный код',
                'Лицензия GNU GPL v3',
                leading=ft.Icon(ft.Icons.OPEN_IN_BROWSER),
                on_click=lambda _: page.launch_url(f'{REPO_URL}')
            ),
            Settings(
                'Сообщить об ошибке',
                'Нужен Github аккаунт',
                leading=ft.Icon(ft.Icons.ERROR),
                on_click=lambda _: page.launch_url(f'{REPO_URL}/issues/new')
            ),
        ),
        SettingsTitle(f'Версия {VERSION}'),
    ], spacing=0,scroll=ft.ScrollMode.AUTO))
    
    return
# legacy menu    
    throw(ft.Column([
        ft.Text('Тема приложения', size=20),
        ft.FilledButton('Сменить цвет', on_click=lambda _: page.open(themechangealert)),
        ft.Container(height=10),
        ft.Text('Данные', size=20),
        ft.Text(f'Расписание будет актуально {TIMEOUT} дн. после чего произойдет обновление во время запуска приложения'),
        ft.Container(height=0),
        timeout_switch,
        ft.FilledButton('Обновить расписание сейчас', on_click=lambda _: updater(page)),
        ft.Text(
            f"Последнее обновление {(datetime.now()-datetime.strptime(page.client_storage.get('date'), '%d/%m/%Y, %H:%M:%S')).days} дн. назад", 
            size=13, 
            color=ft.Colors.SECONDARY    
        ), #type: ignore | always exist
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