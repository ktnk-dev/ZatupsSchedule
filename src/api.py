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
    
def cache(token: str) -> list[float]: #type: ignore
    enpoints = [
        'teachers', 'students/groups',
        'map/rooms', 'schedule/lessons'
    ]
    out = []
    
    for endpoint in enpoints:
        chunks = []
        downloaded = 0

        with httpx.stream('get', f'{BASE_URL}/database/v1/{endpoint}/', headers={'token': token}) as w:
            total_size = int(w.headers.get('content-length', 0))
            
            for chunk in w.iter_raw(chunk_size=8192):
                if not chunk: continue
                chunks.append(chunk)
                downloaded += len(chunk)
                if endpoint == enpoints[-1]:
                    yield (downloaded/total_size) #type: ignore
            
            data = json.loads(b''.join(chunks))
            out.append(data)
    
    Storage.set(out)


    



