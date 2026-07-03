import requests

session = requests.Session()
response = session.get('http://localhost:8000/api/')
csrf_token = response.cookies.get('csrftoken') or session.cookies.get('csrftoken')

login_data = {
    'email': 'ortizpatrick473@gmail.com',
    'password': 'JXE0oR3CIo'
}
headers = {'X-CSRFToken': csrf_token, 'Referer': 'http://localhost:8000/'} if csrf_token else {}
login_res = session.post('http://localhost:8000/api/auth/login/', json=login_data, headers=headers)
print("Login:", login_res.status_code)

if login_res.status_code == 200:
    csrftoken2 = session.cookies.get('csrftoken') or csrf_token
    headers['X-CSRFToken'] = csrftoken2
    res = session.post('http://localhost:8000/api/nomina/generar/', json={'mes': 7, 'ano': 2026}, headers=headers)
    print("Generar:", res.status_code, res.text)
