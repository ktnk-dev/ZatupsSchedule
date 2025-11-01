import flet as ft
from . import Navigator, NavigatorPage

from .settings import updater
from storage import Storage
from components.schedule_display import Schedule

def current_schedule(page: ft.Page, throw):
    list_saved = page.client_storage.get('saved')
    if not list_saved: list_saved = []
    active = page.client_storage.get('active')
    if active not in list_saved: 
        active = None
        page.client_storage.set('active', False)
    
    icons = {
        'teachers': ft.Icons.SCHOOL,
        'rooms': ft.Icons.ROOM,
        'groups': ft.Icons.GROUP
    }
    
    def change(e):
        global active
        index = int(e.data)
        active = page.client_storage.get('saved')[index] #type: ignore
        drawer.selected_index = index
        page.client_storage.set('active', active)
        selected.value = active[0]
        settings.visible = True
        resolveSchedule()
        page.close(drawer)
        page.update()
        
    
    def delete(e):
        global drawer_icons
        active = page.client_storage.get('active')
        print(active, '<-', list_saved)
        list_saved.remove(active)
        page.client_storage.set('active', False)
        page.client_storage.set('saved', list_saved)
        settings.visible = False
        drawer_icons = [ft.NavigationDrawerDestination(label=q[0], icon=icons[q[1]]) for q in list_saved]
        drawer.controls = drawer_root+drawer_icons
        drawer.selected_index = -1
        page.update()
        
    
    settings = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(
                text='Удалить расписание',
                icon=ft.Icons.BLOCK,
                on_click=delete
            ),
            ft.PopupMenuItem(
                text='Обновить расписание',
                icon=ft.Icons.UPDATE,
                on_click=lambda _: updater(page)
            ),
        ]
    )
    settings.visible = bool(active) 
    
    
    c_schedule: ft.Container = ft.Container(expand=True)
    
    def resolveSchedule():  
        a = page.client_storage.get('active')
        if not a: return
        try: db = Storage.extract(a[0].strip()).model_dump()[a[1]]
        except: updater(page)
        print(a[0], Storage.extract(a[0]))
        c_schedule.content = ft.Text('Не удалось найти расписание. Попробуйте пересохранить расписание или обновите данные', color=ft.Colors.ERROR, size=17) \
            if not len(db) else Schedule(page, db[0], a[1], True)
        
        page.update()
        # if len(db):
        #     for q in c_schedule.content.controls: #type: ignore
        #         q.update()
    
    resolveSchedule()

    closeicon = ft.Container(
        ft.Column(
            [
                ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: page.close(drawer)),
            ], horizontal_alignment=ft.CrossAxisAlignment.END
        ),
        on_click=lambda _: page.close(drawer),
        margin=ft.Margin(12,12,12,4)
    )
    drawer_root = [closeicon, ft.Divider()]
    drawer_icons = [ft.NavigationDrawerDestination(label=q[0], icon=icons[q[1]]) for q in list_saved]
    drawer = ft.NavigationDrawer(
        controls=drawer_root+drawer_icons, on_change=change, selected_index=list_saved.index(active) if active else 0
    )
    selected = ft.Text(active[0] if active else 'Выбери расписание', size=18, color=ft.Colors.SECONDARY)
    if not active:
        c_schedule.content = ft.Text('Расписания можно найти во вкладке "Поиск", введя в поисковую строку название группы, номер аудитории или ФИО преподавателя', size=19)
    
    def openDrawer(e):
        global drawer_icons, list_saved
        list_saved = page.client_storage.get('saved')
        if not list_saved: list_saved = []
        drawer_icons = [ft.NavigationDrawerDestination(label=q[0], icon=icons[q[1]]) for q in list_saved] # type: ignore
        drawer.controls = drawer_root+drawer_icons
        page.open(drawer)
        
    
    throw(ft.Column(
        [
            ft.Row([
                ft.Row([
                    ft.IconButton(icon=ft.Icons.LIST, on_click=openDrawer, icon_color=ft.Colors.SECONDARY),
                    selected
                ]),
                settings
                
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            c_schedule
        ]
    ))
    # sleep(.1)
    # page.update()

Navigator.add(
    NavigatorPage(
        label='Расписание',
        icon=ft.Icons.SCHEDULE,
        handler=current_schedule,
        position=0
    )
)