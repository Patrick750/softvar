import urllib.request
import urllib.parse
import json

try:
    # 1. Login
    req_login = urllib.request.Request(
        'http://localhost:8000/api/auth/login/',
        data=json.dumps({'email': 'ortizpatrick473@gmail.com', 'password': 'JXE0oR3CIo'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req_login) as response:
        login_data = json.loads(response.read().decode('utf-8'))
        token = login_data.get('token')
        
    # 2. Generar Nomina
    req_nomina = urllib.request.Request(
        'http://localhost:8000/api/nomina/generar/',
        data=json.dumps({'mes': 7, 'ano': 2026}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': f'Token {token}'}
    )
    with urllib.request.urlopen(req_nomina) as response:
        print("Generar:", response.status, response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
