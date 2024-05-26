import os
import json

def load_token():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config.get('authorization')
    return None

def save_token(token):
    with open(CONFIG_FILE, 'w') as file:
        config = {'authorization': token}
        json.dump(config, file)


CONFIG_FILE = '.config.json'
authorization = load_token()
if not authorization:
    authorization = input("Enter the authorization token (including 'Bearer '): ")
    save_token(authorization)
print("Token is loaded from config")
authorization = load_token()
