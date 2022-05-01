# -*- coding: utf-8 -*-
from genericpath import exists
from random import uniform
from time import sleep
import browser_cookie3
import requests
import os
import textwrap
from datetime import datetime

print('''Default request frequency is 1 beatmap every ~22 seconds to avoid too many request, you can change this in source code
Too many request error retry every ~60 seconds
''')

downloadWait = round(uniform(21, 23), 2)
retryError429 = round(uniform(59, 61), 2)

print('''You can turn off subsequent failed time stamp in Failed.txt by turning
failedTimeStamp = '1' to '0' in source code
''')

print('''Please write your beatmap list like this in a text file

https://osu.ppy.sh/beatmapsets/41823
https://osu.ppy.sh/beatmapsets/39804

Make sure the list is in the same folder as this script
''')

fileExist = False
while not fileExist:
    path = input('Enter the name of your list: ')
    fileExist = exists(path)
    print()
    if not fileExist:
        print('Cannot find file, type it again')
        print()

beatmapList = open(path, 'r')

print('''Note: If you download with video and without video,
you might get duplicate files because website adds [no video]
even if it didn't had video to begin with
''')

video = input('Download video? Y or N: ')
print()

print('''Type '1' to auto detect cookies (Might cause to use wrong cookies if you have multiple browsers. Delete osu.ppy.sh cookies where you are not logged in)
Type '2' to use Firefox cookies
Type '3' to use Chrome cookies
Type '4' to use Chrome cookies (if option 3 don't work this might)
''')

cookie = input('Enter option: ')
print()

while cookie != '1' and cookie != '2' and cookie != '3' and cookie != '4':
    print('Please select one of the option')
    cookie = input('Enter option: ')
    print()


# Show HTTP response
def print_roundtrip(response, *args, **kwargs):
    def format_headers(d):
        return '\n'.join(f'{k}: {v}' for k, v in d.items())
    print(textwrap.dedent('''
        ---------------- request ----------------
        {req.method} {req.url}
        {reqhdrs}

        {req.body}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}

        {res.text}
    ''').format(
        req=response.request,
        res=response,
        reqhdrs=format_headers(response.request.headers),
        reshdrs=format_headers(response.headers),
    ))


failedTimeStamp = '1'
retryDownload = True

for beatmap in beatmapList:
    beatmap = beatmap.strip()
    referer = beatmap

    if video == 'y':
        urlDownload = f'{beatmap}/download'
    else:
        urlDownload = f'{beatmap}/download?noVideo=1'

    if cookie == '1':
        cj = browser_cookie3.load()
    elif cookie == '2':
        cj = browser_cookie3.firefox()
    elif cookie == '3':
        cj = browser_cookie3.chrome()
    else:
        cj = browser_cookie3.chrome(cookie_file=os.path.join(os.path.expandvars(
            "%userprofile%"), 'AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies'))

    url = urlDownload

    while retryDownload:

        # r = requests.get(url, cookies=cj, headers={'referer': referer}, hooks={'response': print_roundtrip})
        r = requests.get(url, cookies=cj, headers={'referer': referer})

        if r.status_code == 200:
            # Skip deleted beatmaps
            if r.headers.get('Content-Disposition') is not None:
                mapName = r.headers.get('Content-Disposition')
                mapName = mapName[21:-2]
                # Illegal characters <>:"/\|?*
                mapName = mapName.replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace(
                    '/', '_').replace('\\', '_').replace('|', '_').replace('?', '_').replace('*', '_')

                if exists(f'./Songs/{mapName}'):
                    print(f'{beatmap} already exist')
                    print('(-, – )…zzzZZZ')
                    sleep(downloadWait)
                else:
                    os.makedirs('./Songs', exist_ok=True)
                    with open(f'./Songs/{mapName}', 'wb') as f:
                        f.write(r.content)
                    print(f'Downloaded {beatmap}')
                    print('(-, – )…zzzZZZ')
                    sleep(downloadWait)
            # Write failed download
            else:
                dateTime = datetime.now()
                dateTimeFailed = dateTime.strftime("%d/%m/%Y %H:%M:%S")
                print(f'Failed to download {beatmap}')
                if exists('Failed.txt'):
                    if failedTimeStamp == '1':
                        failedTimeStamp = '0'
                        with open('Failed.txt', 'a') as f:
                            f.write(f'###Failed to download Beatmaps {dateTimeFailed}### \n')
                    with open('Failed.txt', 'a') as f:
                        f.write(f'{beatmap} status code: {r.status_code}\n')
                else:
                    with open('Failed.txt', 'w') as f:
                        failedTimeStamp = '0'
                        f.write(f'###Failed to download Beatmaps {dateTimeFailed}### \n')
                        f.write(f'{beatmap} status code: {r.status_code}\n')
            break
        elif r.status_code == 429:
            print('Too many request. Retrying...')
            sleep(retryError429)
        else:
            dateTime = datetime.now()
            dateTimeFailed = dateTime.strftime("%d/%m/%Y %H:%M:%S")
            print(f'Failed to download {beatmap}')
            if exists('Failed.txt'):
                if failedTimeStamp == '1':
                    failedTimeStamp = '0'
                    with open('Failed.txt', 'a') as f:
                        f.write(f'###Failed to download Beatmaps {dateTimeFailed}### \n')
                with open('Failed.txt', 'a') as f:
                    f.write(f'{beatmap} status code: {r.status_code}\n')
            else:
                with open('Failed.txt', 'w') as f:
                    failedTimeStamp = '0'
                    f.write(f'###Failed to download Beatmaps {dateTimeFailed}### \n')
                    f.write(f'{beatmap} status code: {r.status_code}\n')
            break

print('Finished downloading')
os.system('pause')
