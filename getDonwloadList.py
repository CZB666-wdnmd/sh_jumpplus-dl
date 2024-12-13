import os
import json
from getSeriesDetail import fetch_series_detail
from getSeriesDetailEpisodeList import fetch_series_detail_episode_list
from getEpisodeViewer import fetch_ep_viewer
from http_req import http_img_dl
from http_req import http_post

def get_all_metadata(series_id):
    title = fetch_series_detail(series_id, True)
    fetch_series_detail_episode_list(series_id, title, True)

    return title

def make_ep_list(title):
    episode_number = 1
    found = True
    db_id = []
    while found:
        filename = os.path.join(title, f"episode_{episode_number}.json")
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)["node"]
                print(filename)
                episode_title = data['title']
                database_id = data['databaseId']
                try:
                    subtitle = data['subtitle']
                except Exception as e:
                    subtitle = ""
                    print("no subtittle")

                out_dir = title+"/"+episode_title+subtitle+"/"
                http_img_dl(data['thumbnailUriTemplate'], out_dir+"thumbnail.jpg")
                db_id.append(database_id)

                episode_number += 1
        else:
            found = False
        episode_number += 1
    
    return db_id

def getPages(db_id, needSave = False):
    url = "https://shonenjumpplus.com/api/v1/graphql?opname=EpisodeViewerConditionallyCacheable"

    payload = {
        "operationName":"EpisodeViewerConditionallyCacheable",
        "variables":{"episodeID":db_id},
        "query":"query EpisodeViewerConditionallyCacheable($episodeID: String!) { episode(databaseId: $episodeID) { id databaseId pageImages { totalCount edges { node { src width height tshirtUrl kirinukiUrl clickableAreas { __typename ...ClickableArea } } } } purchaseInfo { __typename ...PurchaseInfo } } }  fragment ClickableArea on Clickable { __typename appUrl position { __typename ... on PageIndexReadableProductPosition { pageIndex: index } ... on CFIReadableProductPosition { cfi } } ... on ClickableRect { height left top width } }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }"
    }

    response = http_post(url, payload)

    if needSave:
        return response

    pics = response.json()["data"]["episode"]["pageImages"]["edges"]

    pic_src = []

    for i, edge in enumerate(pics):
        node = edge['node']
        url = node['src']

        pic_src.append(url)
    
    return pic_src
        