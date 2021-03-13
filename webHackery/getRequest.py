#!/usr/bin/env python3

import urllib.request

body = urllib.request.urlopen("http://samchapman.dev")

print(body.read())
