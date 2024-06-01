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

def manga_image_dl(url, save_path, pic_token):
    headers = {
        'User-Agent': config.ua,
        'Accept-Encoding': 'gzip',
        'X-GIGA-PAGE-IMAGE-AUTH': pic_token
    }

    proxy = 'http://10.0.0.75:9003'
    proxies = {
        'http': proxy,
        'https': proxy
    }
    
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, proxies=proxies, verify=False)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print("Image downloaded successfully!")
                return True
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to download image. Error: {str(e)}")
        
        retries += 1
        print(f"Retrying ({retries}/{max_retries})...")
        time.sleep(1)  # Wait for 1 second before retrying
        
    print("Failed to download image after multiple attempts.")
    return False