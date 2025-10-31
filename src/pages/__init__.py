from typing import Any
from pydantic import BaseModel
import flet as ft
from time import time


class NavigatorPage(BaseModel):
    label: str
    icon: Any
    selected_icon: Any | None = None
    handler: Any
    position: int
    
_PAGES: list[NavigatorPage] = []

class Navigator:
    @staticmethod
    def add(pg: NavigatorPage):
        _PAGES.append(pg)
        _PAGES.sort(key=lambda _: _.position)
        
    @staticmethod
    def build(root: ft.Page) -> None:
        root.clean()
        safe = ft.SafeArea(content=ft.Container(), expand=True, maintain_bottom_view_padding=False)
        
        
        
            
        def change(e: ft.ControlEvent):
            tm = time()
            def throw(data: ft.Control): 
                safe.content = data
                # safe.update()
                root.update()
                print(f'Switched to "{_PAGES[int(e.data)].label}" in {int((time()-tm)*1000)}ms')#type: ignore
            
            _PAGES[int(e.data)].handler(root, throw) #type: ignore
        
        root.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=r.icon,
                    selected_icon=r.selected_icon,
                    label=r.label,
                ) for r in _PAGES
            ],
            on_change=change
        )
        def _(q): safe.content = q
        _PAGES[0].handler(root, _)
        root.add(safe)
        root.update()
        
    
        