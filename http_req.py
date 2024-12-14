import requests
import config
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def remove_illegal_characters(path):
    # 定义非法字符的正则表达式模式
    invalid_chars = r'[<>:"|?*\x00-\x1F]'  # Windows中的非法字符
    if os.name == 'nt':  # Windows系统
        invalid_chars = r'[<>:"|?*\x00-\x1F]'
    else:  # Linux系统
        invalid_chars = r'[<>:"|?*\x00]'

    # 用正则表达式将非法字符替换为空字符串
    clean_path = re.sub(invalid_chars, '', path)

    return clean_path

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

    response = requests.post(url, headers=json.loads(headers), data=json.dumps(payload), verify=False)
    return response

def http_get(url):
    headers = {
        'User-Agent': config.ua,
        'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'authorization': config.authorization
    }
    headers = json.dumps(headers, ensure_ascii=False, indent=4)

    response = requests.get(url, headers=json.loads(headers), verify=False)
    return response

def http_img_dl(url, save_path):
    url = url.replace("{height}", "999999").replace("{width}", "999999")
    save_path = remove_illegal_characters(save_path)
    print(url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def download_file(url, dest_folder, file_name, auth_token, retries=3):
    headers = {
        'X-GIGA-PAGE-IMAGE-AUTH': auth_token,
        'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'User-Agent': config.ua
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            dest_folder = remove_illegal_characters(dest_folder)
            file_name = remove_illegal_characters(file_name)
            with open(os.path.join(dest_folder, file_name), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
    return False

def download_pic_src(url_list, dest_folder, auth_token):
    max_workers = config.simultaneous_downloads
    retries = config.retry_count

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(download_file, url, dest_folder, f"{i + 1}.jpg", auth_token, retries): url
            for i, url in enumerate(url_list)
        }
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    print(f"Successfully downloaded {url}")
                else:
                    print(f"Failed to download {url} after {retries} attempts")
            except Exception as e:
                print(f"Exception occurred for {url}: {e}")
