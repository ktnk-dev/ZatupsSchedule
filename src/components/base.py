import flet as ft

def row(*args, vertical_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.START, **kwargs):
        return ft.Row(args, vertical_alignment=vertical_alignment, **kwargs)
def col(*args, horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.START, **kwargs):
    return ft.Column(args, horizontal_alignment=horizontal_alignment, **kwargs)
def safe(*args, **kwargs) -> ft.SafeArea:
    return ft.SafeArea(*args, **kwargs)