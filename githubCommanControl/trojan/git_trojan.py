#!/usr/bin/env python3

import json
import base64
import sys
import time
import imp
import random
import threading
import queue
import os

trojan_id = "abc"

trojan_config = "%s.json" % trojan_id
data_path = "data/%s/" % trojan_id
trojan_modules = []
configured = False
task_queue = queue.Queue()