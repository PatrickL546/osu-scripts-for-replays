# -*- coding: utf-8 -*-
from pathlib import Path
import os
replayFilePath = input('Enter path of replay file(s): ')

replayPath = Path(replayFilePath).rglob("*.osr")
for file in replayPath:
    os.startfile(file)
    print(f'Opened {str(file)}')

print('Done!')
os.system('pause')
