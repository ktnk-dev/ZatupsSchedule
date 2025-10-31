import flet as ft
from typing import Literal, Any


from components.schedule_display import Schedule

class SearchResult(ft.Container):
    def __init__(self, page: ft.Page, output: list[dict], data_type: Literal['teachers', 'rooms', 'groups']):
        super().__init__()
        icons = {
            'teachers': ft.Icons.SCHOOL,
            'rooms': ft.Icons.ROOM,
            'groups': ft.Icons.GROUP
        }
        
        def click(data: dict[str, Any], data_type: Literal['teachers', 'rooms', 'groups']):
            def handle(e): 
                sc = Schedule(
                    page, 
                    data,
                    data_type,
                    from_home=False
                )
                bs = ft.BottomSheet(
                    ft.Container(
                        sc,
                        expand=True,
                        padding=ft.Padding(15, 15, 15, 15)
                    ),
                    is_scroll_controlled=True,
                    on_dismiss=lambda _: (page.close(bs), page.remove(bs)),
                )
                sc.closefn(bs)
                page.add(bs)
                page.open(bs)
            
            return handle
        self.expand = True
        self.margin = ft.Margin(0, 10, 0, 0)
        self.content = ft.Column([
            ft.Container(
                ft.Row(
                    [
                        ft.Icon(icons[data_type], color=ft.Colors.SECONDARY),
                        ft.Container(
                            ft.Text(  
                                f"{_['second_name']} {_['first_name']} {_['sur_name']}" \
                                    if data_type == 'teachers' \
                                else f"{_['name']}",
                                color=ft.Colors.SECONDARY
                            ),
                            
                        )
                    ],
                    expand=True,                  
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=10,
                padding=10,
                expand=True,
                on_click=click(_, data_type)
            )
            for _ in output
        ][:30],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )
        
        
            
        
        
    