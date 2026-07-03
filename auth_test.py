import requests

session = requests.Session()
# Check if it uses Session Auth or JWT. Let's try session auth.
# First, we need CSRF.
response = session.get('http://localhost:8000/api/')
csrf_token = response.cookies.get('csrftoken') or session.cookies.get('csrftoken')

login_data = {
    'username': '1118364706',
    'password': 'JXE0oR3CIo' # from the recovery log
}
headers = {'X-CSRFToken': csrf_token, 'Referer': 'http://localhost:8000/'} if csrf_token else {}
# Try to login if there is an endpoint
login_res = session.post('http://localhost:8000/api/auth/login/', json=login_data, headers=headers)
print("Login:", login_res.status_code, login_res.text)

if login_res.status_code == 200:
    token = login_res.json().get('token')
    if token:
        headers['Authorization'] = f'Token {token}'

    res = session.post('http://localhost:8000/api/nomina/generar/', json={'mes': 7, 'ano': 2026}, headers=headers)
    print("Generar:", res.status_code, res.text)
