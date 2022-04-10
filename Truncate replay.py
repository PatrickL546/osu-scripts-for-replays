from pathlib import Path

print('This will remove the first 90 bytes of the replay file\n')

replayFilePath = input('Enter path of replays: ')
print('')

for file in Path(replayFilePath).rglob('*.osr'):
    with open('truncated.log', 'a') as f:
        f.write(str(file) + '\n')
    with open(file, 'rb') as in_file:
        write = in_file.read()[90:]
    with open(file, 'wb') as out_file:
        out_file.write(write)