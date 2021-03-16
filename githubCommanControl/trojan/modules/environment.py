#!/usr/bin/env python3

#This retrieves environment variables set on the machine it runs on

import os

def run(**args):
    print("[*] In environment module.")
    return str(os.environ)