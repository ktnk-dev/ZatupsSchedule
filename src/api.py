import httpx

try: import config
except ImportError: exit('Не указаны переменные в src/config.py')

from config import * 

def authorize() -> str:
    out = httpx.post(
        f'{BASE_URL}/auth/v1/authorize/admin',
        json={
            'login': LOGIN, 
            'password': PASSWORD
        }
    ).json()
    return out['token']


import json
from storage import Storage
VISUAL_SEPARATOR = 4 # X => 1/X

def cache(token: str) -> list[float]: #type: ignore
    enpoints = [
        'teachers', 'students/groups',
        'map/rooms', 'schedule/lessons'
    ]
    out = []
    
    for index, endpoint in enumerate(enpoints):
        chunks = []
        downloaded = 0

        with httpx.stream('get', f'{BASE_URL}/database/v1/{endpoint}/', headers={'token': token}) as w:
            total_size = int(w.headers.get('content-length', 0))
            
            for chunk in w.iter_raw(chunk_size=1024*16):
                if not chunk: continue
                chunks.append(chunk)
                downloaded += len(chunk)
                if index != 3:
                    yield ((downloaded/total_size)+index)/3 /VISUAL_SEPARATOR #type: ignore
                else:
                    yield min(0.99,
                        (
                            (downloaded * ((VISUAL_SEPARATOR-1)/VISUAL_SEPARATOR) )
                            /total_size
                        ) + (1/VISUAL_SEPARATOR)
                    ) #type: ignore
            
            data = json.loads(b''.join(chunks))
            out.append(data)
    
    Storage.set(out)
    yield 1 #type: ignore
    
    
def app_update_required() -> tuple[bool, str]:
    req = httpx.get(REPO_URL.replace('github.com', 'api.github.com/repos') + '/releases')
    origin = req.json()[0]
    required = VERSION != origin['tag_name']
    text = origin['body'] if required else ''
    return (required, text)
    
    



