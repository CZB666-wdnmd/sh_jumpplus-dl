import threading
import requests
from queue import Queue
from time import sleep
import time
import config

class DownloadTask:
    def __init__(self, url, save_path, pic_token, retries=5):
        self.url = url
        self.save_path = save_path
        self.pic_token = pic_token
        self.retries = retries

def manga_image_dl(url, save_path, pic_token, retries):
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
    
    attempts = 0
    while attempts < retries:
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
        
        attempts += 1
        print(f"Retrying ({attempts}/{retries})...")
        time.sleep(1)  # Wait for 1 second before retrying
        
    print("Failed to download image after multiple attempts.")
    return False

def worker(queue):
    while not queue.empty():
        task = queue.get()
        if task is None:
            break
        manga_image_dl(task.url, task.save_path, task.pic_token, task.retries)
        queue.task_done()

class DownloadManager:
    def __init__(self, num_threads=4):
        self.queue = Queue()
        self.num_threads = num_threads
        self.threads = []

    def add_task(self, task):
        self.queue.put(task)

    def start(self):
        for _ in range(self.num_threads):
            thread = threading.Thread(target=worker, args=(self.queue,))
            thread.start()
            self.threads.append(thread)

    def wait_for_completion(self):
        self.queue.join()
        for thread in self.threads:
            thread.join()
