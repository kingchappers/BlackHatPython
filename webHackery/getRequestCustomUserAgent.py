#!/usr/bin/env python3

import urllib.request

url = "https://samchapman.dev"

headers = {}
headers['User-Agent'] = "Googlebot"

request = urllib.request.Request(url,headers=headers)
response = urllib.response.urlopen(request)

print(response.read())
response.close()