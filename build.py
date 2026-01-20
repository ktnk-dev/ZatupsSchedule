#!/usr/bin/env python3
import os
import sys
import time

BASE = 'flet build'
ARGS = '-v'
TARGET = [
    'apk',# --flutter-build-args="--target-platform=android-arm64" --flutter-build-args="--target-platform=android-arm"',
    # 'web'
]

ADB = 'D:\\ADB\\adb.exe'

_start = time.perf_counter()
os.system('uv sync')
for target in TARGET:
    os.system(f'uv run {BASE} {target} {ARGS}')
    if target == 'apk' and sys.platform == 'win32':
        os.system(f'{ADB} install build\\apk\\app-release.apk')
_end = time.perf_counter()
print(f'\n\nBuilded in {int(_end-_start)}s')