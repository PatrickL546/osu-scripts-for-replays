from pathlib import Path
import os
replayFilePath = input('Enter path of replay file(s): ')

replayPath = Path(replayFilePath).rglob("*.osr")
for file in replayPath:
    os.startfile(file)
    print('Opened ' + str(file))

os.system('pause')