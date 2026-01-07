import os
import json

# from pydantic import BaseModel

DATA_PATH = os.getenv("FLET_APP_STORAGE_DATA")
LOADED = []


class Extract():
    teachers: list[dict]
    groups: list[dict]
    rooms: list[dict]
    lessons: list[dict]
    
    def __init__(self, teachers, groups, rooms, lessons) -> None:
        self.teachers = teachers
        self.groups = groups
        self.rooms = rooms
        self.lessons = lessons
    
    def model_dump(self):
        return {
            'teachers': self.teachers,
            'groups': self.groups,
            'rooms': self.rooms,
            'lessons': self.lessons
        }

class Storage:
    @staticmethod
    def get():
        global LOADED
        try:
            if not len(LOADED): 
                with open(os.path.join(DATA_PATH, 'main.json'), 'r', encoding='utf-8') as f: #type: ignore
                    LOADED = json.loads(f.read())
        except: LOADED = []
        return LOADED
    
    @staticmethod
    def set(data: list[list[dict]]):
        global LOADED
        LOADED = data
        with open(os.path.join(DATA_PATH, 'main.json'), 'w', encoding='utf-8') as f: #type: ignore
            f.write(json.dumps(LOADED))
    
    
    @staticmethod
    def extract(query: str | None = None) -> Extract:
        data = LOADED
        if query: query = query.strip()
        if query == '': query = None
        return Extract(
            teachers = data[0] if not query else list(filter(None, [_ if query.lower().strip() in f"{_['second_name']} {_['first_name']} {_['sur_name']}".lower().strip() else False for _ in data[0]])), #type: ignore
            groups = data[1] if not query else list(filter(None, [_ if query.lower() in _['name'].lower() else False for _ in data[1]])), #type: ignore
            rooms = data[2] if not query else list(filter(None, [_ if query.lower() in _['name'].lower() else False for _ in data[2]])), #type: ignore
            lessons = data[3] if not query else list(filter(None, [_ if query in _['teacher_ids'] or query in _['room_ids'] or query in _['group_ids'] else False for _ in data[3]])) #type: ignore
        )