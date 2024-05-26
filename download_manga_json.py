import os
import json
import requests
import config
import re
from retry import retry

def download_all(title):
    
    # 寻找与标题匹配的文件
    episode_number = 1
    found = True
    while found:
        filename = os.path.join(title, f"episode_{episode_number}.json")
        if os.path.exists(filename):
            found = True
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)["node"]
                print(filename)
                # 解析所需字段
                accessibility = data['accessibility']
                published_at = data['publishedAt']
                episode_id = data['id']
                episode_title = data['title']
                database_id = data['databaseId']
                if accessibility == "READABLE":
                    episode_number += 1
                    subtitle = "" if data.get('subtitle') == "null" else ' ' + data.get('subtitle')
                    thumbnail_uri_template = data['thumbnailUriTemplate']
                    # 返回所需字段
                    out_dir = title+"/"+episode_title+subtitle+"/"
                    print("downloading episode" + str(episode_number))
                    download(database_id, out_dir)
                    continue
                print("Skip not free" + episode_title)
                episode_number += 1
        else:
            found = False
        episode_number += 1
    
    # 如果未找到匹配的标题
    return None

def download_one(ep, title):
    print('todo')

@retry(Exception, tries=3, delay=2, backoff=2)
def send_http_request(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果响应状态码不是 200，将会抛出异常
    return response

def save_image(url, save_path, pic_token):
    headers = {
        'User-Agent': 'ShonenJumpPlus-Android/4.0.4 (Android 14/34/2210132G/UKQ1.230804.001 release-keys)',
        'Accept-Encoding': 'gzip',
        'X-GIGA-PAGE-IMAGE-AUTH': pic_token
    }

    try:
        response = send_http_request(url, headers)
    except Exception as e:
        print("failed")
    
    with open(save_path, 'wb') as f:
        f.write(response.content)

def remove_illegal_characters(path):
    # 定义非法字符的正则表达式模式
    invalid_chars = r'[<>:"|?*\x00-\x1F]'  # Windows中的非法字符

    # 用正则表达式将非法字符替换为空字符串
    clean_path = re.sub(invalid_chars, '', path)

    return clean_path

def download(db_id, out_dir):
    authorization = config.authorization

    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=EpisodeViewer'
    headers = {
        'User-Agent': 'ShonenJumpPlus-Android/4.0.4 (Android 14/34/2210132G/UKQ1.230804.001 release-keys)',
        'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-apollo-operation-id': '655c41075ff2c491e7b8338a7fb3407782a5e9b4beb6e2397ef330e15d72e34a',
        'x-apollo-operation-name': 'SeriesDetail',
        'x-giga-device-id': '20a24c1ed9ed1d39',
        'authorization': authorization
    }
    
    payload = {
        "operationName": "EpisodeViewer",
        "variables": {"episodeID": db_id},
        "query": "query EpisodeViewer($episodeID: String!) { episode(databaseId: $episodeID) { pageImageToken  } }"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    pic_token = response.json()["data"]["episode"]["pageImageToken"]

    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=EpisodeViewerConditionallyCacheable'
    headers = {
        'User-Agent': 'ShonenJumpPlus-Android/4.0.4 (Android 14/34/2210132G/UKQ1.230804.001 release-keys)',
        'Accept': 'multipart/mixed; deferSpec=20220824, application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-apollo-operation-id': '655c41075ff2c491e7b8338a7fb3407782a5e9b4beb6e2397ef330e15d72e34a',
        'x-apollo-operation-name': 'SeriesDetail',
        'x-giga-device-id': '20a24c1ed9ed1d39',
        'authorization': authorization
    }
    
    payload = {
        "operationName": "EpisodeViewerConditionallyCacheable",
        "variables": {"episodeID": db_id},
        "query": "query EpisodeViewerConditionallyCacheable($episodeID: String!) { episode(databaseId: $episodeID) { id databaseId pageImages { totalCount edges { node { src width height tshirtUrl clickableAreas { __typename ...ClickableArea } } } } purchaseInfo { __typename ...PurchaseInfo } } }  fragment ClickableArea on Clickable { __typename appUrl position { __typename ... on PageIndexReadableProductPosition { pageIndex: index } ... on CFIReadableProductPosition { cfi } } ... on ClickableRect { height left top width } }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    pic_json = response.json()["data"]["episode"]["pageImages"]
    pic_count = str(pic_json["totalCount"])

    clean_out_dir = remove_illegal_characters(out_dir)
    if not os.path.exists(clean_out_dir):
        os.makedirs(clean_out_dir)

    # 解析JSON数据
    pics = response.json()["data"]["episode"]["pageImages"]["edges"]
    
    
    for i, edge in enumerate(pics):
        node = edge['node']
        url = node['src']

        save_path = clean_out_dir+str(i + 1).zfill(len(pic_count))+".png"
        
        save_image(url, save_path, pic_token)