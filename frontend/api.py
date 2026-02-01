import requests

Base_url = "http://127.0.0.1:8000"

def login_user(email,password):
    url = f"{Base_url}/auth/login"
    payload = {
        "email": email,
        "password":password
    }
    response = requests.post(url,json=payload)
    return response
