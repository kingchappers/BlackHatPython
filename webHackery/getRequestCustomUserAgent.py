#!/usr/bin/env python3

import urllib.request

url = "https://samchapman.dev"

#Setting up the headers and making this appear as though it's a Googlebot via the user agent 
headers = {}
headers['User-Agent'] = "Googlebot"

request = urllib.request.Request(url,headers=headers)
response = urllib.request.urlopen(request)

print(response.read())
response.close()