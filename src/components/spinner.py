import os
import flet as ft
from time import sleep
from storage import Storage
from datetime import datetime

def spinner_fulscreen(page: ft.Page, *args):    
    def ignore_update(e):
        page.client_storage.set('date', datetime.now().strftime('%d/%m/%Y, %H:%M:%S'))
        def destroy(e):
            os._exit(0)
            #page.window.destroy()
            #os._exit(0)

        banner = ft.AlertDialog(
            modal=False,
            title=ft.Text("Пропуск обновления"),
            content=ft.Row([
                ft.Text("Требуется перезапуск приложения"),
                
            ], wrap=True),
            actions=[
#                 ft.FilledButton("Продолжить", on_click=destroy, bgcolor=ft.Colors.RED),
            ],
            on_dismiss=destroy
        )
        page.add(banner)
        page.open(banner)
        page.update()
#         destroy(False)
    
    pb = ft.ProgressRing()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.clean()
    page.add(ft.SafeArea(
        ft.Container(
            ft.Row(
                [ft.Column(
                    [pb]+list(args)+[
                        ft.Text('', size=15),
                        ft.FilledButton('Пропустить', on_click=ignore_update, bgcolor=ft.Colors.ERROR) if len(Storage.get())>1 else ft.Text('', size=1)
                    ],
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

