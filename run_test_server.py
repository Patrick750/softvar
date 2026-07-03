import requests
import time
import subprocess
import threading

def start_server():
    return subprocess.Popen(["venv/bin/python", "manage.py", "runserver", "8080"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

server = start_server()
time.sleep(3)

# We need a token or we can just read the stderr output after making a request
# Let's write a script to reproduce the error by calling the function directly
