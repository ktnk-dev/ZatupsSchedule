from typing import Any
import flet as ft
from time import time
from components.selfdantic import BaseModel

class NavigatorPage(BaseModel):
    label: str
    icon: Any
    selected_icon: Any | None = None
    handler: Any
    position: int
    
_PAGES: list[NavigatorPage] = []
_ACTIVE_PAGE: int = -1

class Navigator:
    @staticmethod
    def add(pg: NavigatorPage):
        _PAGES.append(pg)
        _PAGES.sort(key=lambda _: _.position)
        
    @staticmethod
    def build(root: ft.Page) -> None:
        root.clean()
        safe = ft.SafeArea(
            content=ft.AnimatedSwitcher(
                ft.Container(),
                transition=ft.AnimatedSwitcherTransition.FADE,
                duration=150,
            ), 
            expand=True, 
            maintain_bottom_view_padding=False
        )
        
        def change(e: ft.ControlEvent):
            global _ACTIVE_PAGE
            if _ACTIVE_PAGE == int(e.data): return
            _ACTIVE_PAGE = int(e.data)
            safe.content.content.clean() #type: ignore | always exist
            tm = time()
            def throw(data: ft.Control): 
                safe.content.content = data #type: ignore | always exist
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
        def _(q): safe.content.content = q #type: ignore | always exist
        _PAGES[0].handler(root, _)
        root.add(safe)
        root.update()
        
    
        