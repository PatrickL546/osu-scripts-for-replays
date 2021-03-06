# -*- coding: utf-8 -*-
from genericpath import exists
from random import uniform
from time import sleep
import requests
import os
import textwrap
from datetime import datetime
import json


def WriteFailed():
    failedTimeStamp = '1'

    dateTime = datetime.now()
    dateTimeFailed = dateTime.strftime("%d/%m/%Y %H:%M:%S")

    print(f'Failed to get beatmap for: {hash}')

    if exists('Failed.txt'):
        if failedTimeStamp == '1':
            failedTimeStamp = '0'
            with open('Failed.txt', 'a') as f:
                f.write(f'###Failed to get Beatmaps URL from hash {dateTimeFailed}###\n')
        with open('Failed.txt', 'a') as f:
            f.write(f'{hash} status code: {r.status_code}\n')
    else:
        with open('Failed.txt', 'w') as f:
            failedTimeStamp = '0'
            f.write(f'###Failed to get Beatmaps URL from hash {dateTimeFailed}###\n')
            f.write(f'{hash} status code: {r.status_code}\n')


print('''Default request frequency is 60 MD5 hash every ~60 seconds to avoid too many request, you can change this in source code
Too many request error retry every ~60 seconds
''')

requestWait = round(uniform(0, 2), 2)
retryError429 = round(uniform(59, 61), 2)

print('''You can turn off subsequent failed time stamp in Failed.txt by turning
failedTimeStamp = '1' to '0' in source code
''')

print('''You may request an API key from https://osu.ppy.sh/p/api/
API key looks like this: 1234a56d45a6b456b789b123654d654f654f654q
''')

apiKey = input('Enter your api key: ')
print()

print('''Please write your MD5 hash list like this in a text file

2d687e5ee79f3862ad0c60651471cdcc
da8aae79c8f3306b5d65ec951874a7fb

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

MD5HashList = open(path, 'r')


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


retryDownload = True

for hash in MD5HashList:
    hash = hash.strip()
    url = f'https://osu.ppy.sh/api/get_beatmaps?k={apiKey}&h={hash}'

    while retryDownload:

        # r = requests.get(url, hooks={'response': print_roundtrip})
        r = requests.get(url)
        rText = r.text

        if r.status_code == 200:
            # Skip deleted beatmaps
            if 'beatmapset_id' in rText:
                content = json.loads(rText)
                beatmapID = content[0]['beatmapset_id']
                beatmapURL = f'https://osu.ppy.sh/beatmapsets/{beatmapID}'

                if exists('Beatmap list.txt'):
                    # Check if Beatmap URL already exist in list
                    with open('Beatmap list.txt', 'r') as f:
                        if beatmapURL in f.read():
                            print(f'{beatmapURL} already exist')
                        else:
                            with open('Beatmap list.txt', 'a') as f:
                                f.write(f'{beatmapURL}\n')
                                print(f'Get URL: {beatmapURL}')
                                print('(-, ??? )???zzzZZZ')
                                sleep(requestWait)
                else:
                    with open('Beatmap list.txt', 'w') as f:
                        f.write(f'{beatmapURL}\n')
                        print(f'Get URL: {beatmapURL}')
                        print('(-, ??? )???zzzZZZ')
                        sleep(requestWait)
            else:
                WriteFailed()
            break
        elif r.status_code == 429:
            print('Too many request. Retrying...')
            sleep(retryError429)
        else:
            WriteFailed()
            break

print('Done!')
os.system('pause')
