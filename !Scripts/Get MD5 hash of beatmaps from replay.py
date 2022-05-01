from pathlib import Path
import os
replayFilePath = input('Enter path of replay file(s): ')
replayHash = []

replayPath = Path(replayFilePath).rglob("*.osr")
for file in replayPath:
    with open(file, 'rb') as f:
        md5Hash = f.read()[7:39]
        print("Beatmap MD5: " + str(md5Hash,"utf-8") + 'for ' + str(file))
        replayHash.append(md5Hash)

replayHash = list(set(replayHash))

with open('MD5.txt','w') as f:
    for hash in replayHash:
        f.write(str(hash,"utf-8") + '\n')

os.system('pause')