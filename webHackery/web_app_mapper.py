#!/usr/bin/env python3

import urllib.request
#queue objects allow us to build a large, thread-safe, stack of items and have threads pick them up for processing
import queue
import threading
import os

threads = 10

#define the target website and the directory we've downloaded the web application to 

target = "http://www.blackhatpython.com"
directory = "~/Downloads/joomla-3.1.1"
#file extensions we don't want to fingerprint
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

#queue object that store the files we're trying to locate on the remote server
web_paths = queue.Queue()

#Walk through the files and directories in the local web app directory
#While walking through the files it builds the full path to the target files and tests them against the filter list
#Each valid file is added to the queue
for r,d,f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r,files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty:
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib.request.Request(url)

        try:
            response = urllib.request.urlopen(request)
            content = response.read()

            print("[%d] => %s" % (response.code, path))
            response.close()

        except urllib.request.HTTPError as error:
            print("Failed %s" % error.code)
            pass
    
    for i in range(threads):
        print("Spawning thread: %d" % i)
        t = threading.Thread(target = test_remote)
        t.start()