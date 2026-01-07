#!/usr/bin/env python3
import os
import sys

ADB = 'D:\\ADB\\adb.exe'
TARGET = [
    'apk',
    # 'web'
]

os.system('uv sync')
for target in TARGET:
    os.system(f'uv run flet build {target}')
    if target == 'apk' and sys.platform == 'win32':
        os.system(f'{ADB} install build\\apk\\app-release.apk')
