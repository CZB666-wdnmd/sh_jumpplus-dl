import requests
import config
import json

def http_post(url, payload, headers_add={}):
    headers_add = json.load(headers_add)
    headers = {
        'User-Agent': config.ua,
        'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'authorization': config.authorization
    }
    headers.update(headers_add)
    headers = json.dump(headers, ensure_ascii=False, indent=4)

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response

def http_img_dl(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        response.raise_for_status()

def manga_image_dl(url, save_path, pic_token):
    headers = {
        'User-Agent': 'ShonenJumpPlus-Android/4.0.4 (Android 14/34/2210132G/UKQ1.230804.001 release-keys)',
        'Accept-Encoding': 'gzip',
        'X-GIGA-PAGE-IMAGE-AUTH': pic_token
    }

    response = requests.get(url, headers)
    
    with open(save_path, 'wb') as f:
        f.write(response.content)