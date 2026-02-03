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

def predict_garbage(uploaded_file, token):
    url = f"{Base_url}/predict"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type,
        )
    }

    response = requests.post(url, headers=headers, files=files)
    return response
