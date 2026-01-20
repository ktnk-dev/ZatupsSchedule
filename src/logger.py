import flet as ft
from datetime import datetime

_STARTUP_TIME = datetime.now()
_SAVED_LOGS = []
def _add_log(**kwargs):
    kwargs['dt'] = datetime.now()
    _SAVED_LOGS.append(kwargs)

def log(name, text):_add_log(name=name, text=text, action='log')
def warn(name, text):_add_log(name=name, text=text, action='warn')
def error(name, text):_add_log(name=name, text=text, action='error')
def display(page: ft.Page):
    def c(l):
        ICONS = {
            'log': ft.Icons.ARROW_RIGHT_ROUNDED,
            'warn': ft.Icons.WARNING,
            'error': ft.Icons.ERROR
        }
        COLORS = {
            'log': None,
            'warn': ft.Colors.YELLOW,
            'error': ft.Colors.RED
        }
        T = l["dt"]-_STARTUP_TIME
        return ft.Row(
            [
                ft.ListTile(
                    title=ft.Text(l['name'],color=COLORS[l['action']]),
                    leading=ft.Icon(ICONS[l['action']], color=COLORS[l['action']]),
                    subtitle=ft.Text(l['text']),
                    expand=True
                ),
                ft.Text(f'{round(T.seconds+T.microseconds/1000000,4)}s', color=ft.Colors.SECONDARY) #if on_click else ft.Container()
            ], vertical_alignment = ft.CrossAxisAlignment.CENTER
        )
    
    bs = ft.BottomSheet(
        ft.Container(
            ft.Column([
                c(i) for i in _SAVED_LOGS[::-1]
            ]),
            expand=True,
            padding=15
        ),
        is_scroll_controlled=True,
        enable_drag=True,
        use_safe_area=True,
        on_dismiss=lambda _: (page.close(bs), page.remove(bs)),
    )
    page.add(bs)
    page.open(bs)
