import flet as ft
from time import sleep
from typing import Literal, Any
from storage import Storage
from datetime import datetime

class Schedule(ft.Column):
    def __init__(self, page: ft.Page, data: dict, data_type: Literal['teachers', 'rooms', 'groups'], from_home: bool):
        super().__init__()
        self.page = page
        icons = {
            'teachers': ft.Icons.SCHOOL,
            'rooms': ft.Icons.ROOM,
            'groups': ft.Icons.GROUP
        }
        self.um = lambda _: True
        
        schedule = Storage.extract(data['id']).lessons
        self.expand = True
        
        if not len(schedule):
            self.controls = [
                ft.Text('', size=20),
                ft.Icon(ft.Icons.BLOCK, color=ft.Colors.ERROR, size=40),
                ft.Text('', size=1),
                ft.Text('Не удалось найти пары', color=ft.Colors.ERROR, size=20, text_align=ft.TextAlign.CENTER),
                ft.Text('', size=1),
                ft.FilledButton('Закрыть', on_click=lambda _:self.um(_), bgcolor=ft.Colors.ERROR) if not from_home else ft.Text('')
            ]
            self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            return
        
        self.controls = []
        name = f"{data['second_name']} {data['first_name']} {data['sur_name']}" \
                if data_type == 'teachers' \
            else f"{data['name']}"
        
        # page.client_storage.set('saved', [])
        list_saved = page.client_storage.get('saved')
        if not list_saved: list_saved = []
        
        def add_saved(e): 
            list_saved.append([name, data_type])
            page.client_storage.set('saved', list_saved)
            if not page.client_storage.get('active'): 
                page.client_storage.set('active', [name, data_type])
            
            act_button.text = 'Удалить '
            act_button.icon = ft.Icons.BLOCK
            act_button.on_click = remove_saved
            act_button.bgcolor = ft.Colors.RED
            self.update()
            page.update()
            print(list_saved)
                
        def remove_saved(e): 
            list_saved.remove([name, data_type])
            page.client_storage.set('saved', list_saved)
            
            act_button.text = 'Сохранить '
            act_button.icon = ft.Icons.ADD
            act_button.on_click = add_saved
            act_button.bgcolor = ft.Colors.PRIMARY
            self.update()
            page.update()
            print(act_button.text)
            print(list_saved)
                
            
        add_saved_button = ft.FilledButton('Сохранить ', icon=ft.Icons.ADD, on_click=add_saved, bgcolor=ft.Colors.PRIMARY) 
        remove_saved_button = ft.FilledButton('Удалить ', icon=ft.Icons.BLOCK, on_click=remove_saved, bgcolor=ft.Colors.RED) 
        
        act_button = remove_saved_button if [name, data_type] in list_saved else add_saved_button
            
        if not from_home:
            def close(e): 
                self.um(e)
                
                
                
            self.controls.append(
                ft.Column([
                    ft.Row(
                        [
                            ft.Text('Расписание', size=20),
                            ft.Row(
                                [act_button, ft.IconButton(ft.Icons.CLOSE, on_click=close)],   
                                alignment=ft.MainAxisAlignment.END
                            ),
                        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row([
                        ft.Text(
                            name,
                            size=20,
                            # color=ft.Colors.SECONDARY
                        )  
                    ]),
                ],   
                )
            )

        def generateday(weekday: int, is_odd: bool):
            ls = list(filter(lambda _: _['weekday'] == weekday and (_['is_odd_week' if not is_odd else 'is_even_week'] == False or _['is_odd_week'] == _['is_even_week']), schedule)) #type: ignore
            ls.sort(key=lambda _: _['time_start'])
            
            def lesson(d: dict):
                def openself(obj, type):
                    def handle(e):
                        sc = Schedule(
                            page,
                            obj,
                            type,
                            from_home=False
                        )
                        bs = ft.BottomSheet(
                            ft.Container(
                                sc,
                                expand=True,
                                padding=15
                            ),
                            is_scroll_controlled=True,
                            enable_drag=True,
                            use_safe_area=True,
                            on_dismiss=lambda _: (page.close(bs), page.remove(bs)),
                        )
                        sc.closefn(bs)
                        page.add(bs)
                        page.open(bs)
                        
                    return handle
                        
                def gentime(): return f"{d['time_start']//60}:{d['time_start']%60:0>2}"
                empty = None
                return ft.Container(
                    ft.Column(list(filter(None, [ #type: ignore
                        ft.Text(f"{d['type']} в {gentime()}", color=ft.Colors.SECONDARY, size=13),
                        ft.Text(d['name'], size=16),
                        
                        
                        ft.Text('', size=7) if len(d['rooms']) and data_type != 'rooms' else empty,
                        ft.Text('Аудитории', color=ft.Colors.SECONDARY, size=13) if len(d['rooms']) and data_type != 'rooms' else empty,
                        ft.Text('', size=2) if len(d['rooms']) and data_type != 'rooms' else empty,
                        ft.Row([
                            ft.FilledButton(_['name'], scale=.9, on_click=openself(_, 'rooms'))
                            for _ in d['rooms']
                        ], spacing=2, wrap=True) if len(d['rooms']) and data_type != 'rooms' else empty,
                        # ft.Text('', size=5) if len(d['rooms']) and data_type != 'rooms' else empty,
                        
                        
                        ft.Text('', size=7) if len(d['groups']) and data_type != 'groups' else empty,
                        ft.Text('Группы', color=ft.Colors.SECONDARY, size=13) if len(d['groups']) and data_type != 'groups' else empty,
                        ft.Text('', size=2) if len(d['groups']) and data_type != 'groups' else empty,
                        ft.Row([
                            ft.FilledButton(_['name'], scale=.9, on_click=openself(_, 'groups'))
                            for _ in d['groups']
                        ], spacing=2, wrap=True) if len(d['groups']) and data_type != 'groups' else empty,
                        # ft.Text('', size=5) if len(d['groups']) and data_type != 'groups' else empty,
                        
                        
                        ft.Text('', size=7) if len(d['teachers']) and data_type != 'teachers' else empty,
                        ft.Text('Преподаватели', color=ft.Colors.SECONDARY, size=13) if len(d['teachers']) and data_type != 'teachers' else empty,
                        ft.Text('', size=2) if len(d['teachers']) and data_type != 'teachers' else empty,
                        ft.Row([
                            ft.FilledButton(f"{_['second_name']} {_['first_name'][0]}. {_['sur_name'][0]}.", scale=.9, on_click=openself(_, 'teachers'))
                            for _ in d['teachers']
                        ], spacing=0, wrap=True) if len(d['teachers']) and data_type != 'teachers' else empty,
                        
                        
                    ])), spacing=1, expand=True, width=1000),
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    expand=True
                )
                
            return ft.Container(ft.Column(
                [lesson(_) for _ in ls] if len(ls) else [ft.Text('Пар нет', size=15)], expand=True, scroll=ft.ScrollMode.ADAPTIVE  #type: ignore
            ), padding=ft.Padding(0, 10, 0, 0), expand=True, )
        
        
        dt = datetime.now()
        is_odd = dt.isocalendar()[1]%2 == 1
        week_values = ft.Column()
        week_strings = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

        global week_odd_state
        week_odd_state = not is_odd
        
        def updateweekodd(e):
            global week_odd_state
            week_odd_state = not week_odd_state
            week_switch_odd.selected = week_odd_state
            week_switch_even.selected = not week_odd_state
            week_values.controls = [
                ft.Column([
                    ft.Text('', size=5),
                    ft.Text(w, size=25),
                    generateday(i, week_odd_state),
                ], spacing=0)
                for i, w in enumerate(week_strings)
            ]
            try: page.update()
            except: pass
        
       
        week_switch_odd = ft.Chip(label=ft.Text('Нечетная'), selected=is_odd, on_click=updateweekodd)
        week_switch_even = ft.Chip(label=ft.Text('Четная'), selected=not is_odd, on_click=updateweekodd)
        week_switch = ft.Row([
            week_switch_odd,
            week_switch_even,
        ])
        updateweekodd(None)

        self.tabs = ft.Tabs(
                tabs = [
                    # ft.Tab('dbg', ft.Text('123445')),
                    ft.Tab('Сегодня', generateday(dt.weekday(), is_odd)),
                    ft.Tab('Завтра', generateday((dt.weekday()+1)%7, is_odd if dt.weekday() != 6 else not is_odd)),
                    ft.Tab('На неделю', ft.Column([
                        ft.Text('', size=5), 
                        ft.Text('Текущая неделя выбрана автоматически', size=13, color=ft.Colors.SECONDARY), 
                        week_switch, 
                        week_values,
                    ], expand=True, scroll=ft.ScrollMode.AUTO)),
                ],
                # scrollable=False,
                selected_index=0,
                expand=True
            )
            
        
        self.controls.append(self.tabs)
    def closefn(self, component):
        self.um = lambda _: (self.page.close(component), self.page.remove(component)) #type: ignore
        