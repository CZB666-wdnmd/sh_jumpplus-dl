import os
import json
import re
from http_req import http_post,manga_image_dl
from image_dl import DownloadManager, DownloadTask

def download_all(title):
    # 寻找与标题匹配的文件
    episode_number = 1
    found = True
    while found:
        filename = os.path.join(title, f"episode_{episode_number}.json")
        if os.path.exists(filename):
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
                    try:
                        subtitle = data['subtitle']
                    except Exception as e:
                        subtitle = ""
                        print("no subtittle")
                    thumbnail_uri_template = data['thumbnailUriTemplate']
                    # 返回所需字段
                    out_dir = title+"/"+episode_title+subtitle+"/"
                    print("downloading episode" + str(episode_number))
                    print(out_dir)
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

def remove_illegal_characters(path):
    # 定义非法字符的正则表达式模式
    invalid_chars = r'[<>:"|?*\x00-\x1F]'  # Windows中的非法字符

    # 用正则表达式将非法字符替换为空字符串
    clean_path = re.sub(invalid_chars, '', path)

    return clean_path

def download(db_id, out_dir):
    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=EpisodeViewer'
    
    payload = {
        "operationName": "EpisodeViewer",
        "variables": {"episodeID": db_id},
        "query": "query EpisodeViewer($episodeID: String!) { episode(databaseId: $episodeID) { pageImageToken  } }"
    }

    response = http_post(url, payload)
    pic_token = response.json()["data"]["episode"]["pageImageToken"]

    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=EpisodeViewerConditionallyCacheable'
    
    payload = {
        "operationName": "EpisodeViewerConditionallyCacheable",
        "variables": {"episodeID": db_id},
        "query": "query EpisodeViewerConditionallyCacheable($episodeID: String!) { episode(databaseId: $episodeID) { id databaseId pageImages { totalCount edges { node { src width height tshirtUrl clickableAreas { __typename ...ClickableArea } } } } purchaseInfo { __typename ...PurchaseInfo } } }  fragment ClickableArea on Clickable { __typename appUrl position { __typename ... on PageIndexReadableProductPosition { pageIndex: index } ... on CFIReadableProductPosition { cfi } } ... on ClickableRect { height left top width } }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }"
    }

    response = http_post(url, payload)
    
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
        
        manga_image_dl(url, save_path, pic_token)

        manager = DownloadManager(num_threads=4)
        manager.add_task(DownloadTask(url, save_path, pic_token))

    manager.start()
    manager.wait_for_completion()
