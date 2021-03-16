#!/usr/bin/env python3

#This lists files in the current direcory and returns the list
import os

def run(**args):
    print("[*] In dirlister module.")
    files = os.listdir(".")

    return str(files)