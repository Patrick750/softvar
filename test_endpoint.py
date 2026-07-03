import requests
import json
import time
import subprocess
import os

proc = subprocess.Popen(["venv/bin/python", "manage.py", "runserver", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(2)

# We need to authenticate.
# Or just look at the server output by letting it run and we make the request
