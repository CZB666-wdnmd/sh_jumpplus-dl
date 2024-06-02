import requests
import config
import json
import time

def http_post(url, payload, headers_add="{}"):
    headers_add = json.loads(headers_add)
    headers = {
        'User-Agent': config.ua,
        'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'authorization': config.authorization
    }
    headers.update(headers_add)
    headers = json.dumps(headers, ensure_ascii=False, indent=4)

    proxy = 'http://10.0.0.75:9003'
    proxies = {
        'http': proxy,
        'https': proxy
    }

    response = requests.post(url, headers=json.loads(headers), data=json.dumps(payload), proxies=proxies, verify=False)
    return response

def http_img_dl(url, save_path):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        response.raise_for_status()

