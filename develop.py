#!/usr/bin/env python

import os
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVE_FILE = os.path.join(PROJECT_DIR, 'serve.py')

if __name__ == '__main__':
    while 1:
        subprocess.call(['python', SERVE_FILE])
