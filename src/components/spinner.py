import flet as ft
from time import sleep

def spinner_fulscreen(page: ft.Page, *args):
    restore = page.vertical_alignment.__copy__()
    pb = ft.ProgressRing()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.clean()
    page.add(ft.SafeArea(
        ft.Container(
            ft.Row(
                [ft.Column(
                    [pb]+list(args),
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    expand=1
                )],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=1
            ),
            
        )
    ))
    page.update()    
    return pb

