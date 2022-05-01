import os
import requests
import textwrap


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
url = 'https://www.facebook.com/'
r = requests.get(url, hooks={'response': print_roundtrip})

os.system('pause')
