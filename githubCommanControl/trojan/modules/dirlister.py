#!/usr/bin/env python3

import os

def run(**args):
    print("[*] In dirlister module.")
    files = os.listdir(".")

    return str(files)