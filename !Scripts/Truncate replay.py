from pathlib import Path
import os

print('This will remove the first 90 bytes of the replay file. This makes it possible to use hashing to check for duplicate replay files\n')

replayFilePath = input('Enter path of replays: ')
print('')

for file in Path(replayFilePath).rglob('*.osr'):
    with open(file, 'rb') as in_file:
        write = in_file.read()[90:]

    with open(file, 'wb') as out_file:
        out_file.write(write)

print('Done!')
os.system('pause')