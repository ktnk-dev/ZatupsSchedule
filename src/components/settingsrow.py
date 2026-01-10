import flet as ft
from typing import Any

def Settings(
    title: str,
    subtitle: str,
    leading = None,
    on_click = None,
    item: Any = ft.Icon(ft.Icons.ARROW_RIGHT_ROUNDED, color=ft.Colors.SECONDARY)
) -> ft.Container:
    return ft.Container(
        ft.Row(
            [
                ft.ListTile(
                    title=ft.Text(title),
                    leading=leading,
                    subtitle=ft.Text(subtitle),
                    expand=True
                ),
                item #if on_click else ft.Container()
            ], vertical_alignment = ft.CrossAxisAlignment.CENTER
        ),
        on_click=on_click,
        padding=ft.Padding(4,4,14,6),
        ink=True if on_click else False
#         expand=True
    )

def SettingsContainer(*settings: ft.Container) -> tuple[ft.Container] | tuple[()]:
    BORDER_RADIUS = 15
    if len(settings) == 0: return settings
    settings[0].border_radius = ft.BorderRadius(BORDER_RADIUS,BORDER_RADIUS,0,0)
    if len(settings) > 1: settings[-1].border_radius = ft.BorderRadius(0,0,BORDER_RADIUS,BORDER_RADIUS)
    else: settings[0].border_radius = BORDER_RADIUS
    for _ in settings: _.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
    return settings
    

def SettingsTitle(text: str) -> ft.Container:
    return ft.Container(
        ft.Text(
            text, 
            size=15, 
            # color=ft.Colors.SECONDARY
        ),
        padding=ft.Padding(5, 20, 5, 10),
#         bgcolor=ft.Colors.RED
    )
    