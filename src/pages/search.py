import flet as ft

import api
from components.search_result import SearchResult
from components.spinner import spinner_fulscreen
from . import Navigator, NavigatorPage
from storage import Storage

def current(page: ft.Page, throw):    
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    def search(e):
        q = query.value.strip().lower() # type: ignore
        
        groups_tab.visible = False
        rooms_tab.visible = False
        teachers_tab.visible = False
        
        if len(q) > 1:
            out = Storage.extract(q)
            if len(out.teachers):
                teachers_tab.visible = True
                teachers_tab.content = SearchResult(
                    page, out.teachers, 'teachers'
                )
                
            if len(out.rooms):
                rooms_tab.visible = True
                rooms_tab.content = SearchResult(
                    page, out.rooms, 'rooms'
                )
                
            if len(out.groups):
                groups_tab.visible = True
                groups_tab.content = SearchResult(
                    page, out.groups, 'groups'
                )
                
        page.update()
    
    query = ft.SearchBar(
        # label='Поиск',
        bar_hint_text='Введи группу, аудиторию или ФИО',
        # border=ft.InputBorder.UNDERLINE,
        # filled=False,
        # expand=True,
        on_change=search
    )
    groups_tab = ft.Tab(
        text='Группы',
        # icon=ft.Icon(ft.Icons.GROUP),
        visible=False,
    )
    rooms_tab = ft.Tab(
        text='Аудитории',
        # icon=ft.Icon(ft.Icons.ROOM),
        visible=False,
    )
    teachers_tab = ft.Tab(
        text='Преподаватели',
        # icon=ft.Icon(ft.Icons.SCHOOL),
        visible=False,
    )
    throw(ft.Column(
        [
            query,
            ft.Tabs(
                [groups_tab, rooms_tab, teachers_tab],
                expand=True,
                # scrollable=False,
            )
        ],
        expand=True
    ))
            


Navigator.add(
    NavigatorPage(
        label='Поиск',
        icon=ft.Icons.SEARCH,
        handler=current,
        position=2
    )
)