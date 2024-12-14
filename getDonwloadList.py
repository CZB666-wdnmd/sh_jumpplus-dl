import os
import json
from getSeriesDetail import fetch_series_detail
from getSeriesDetailEpisodeList import fetch_series_detail_episode_list
from getEpisodeViewer import fetch_ep_viewer
from http_req import http_img_dl
from http_req import http_post
from http_req import remove_illegal_characters

def make_ep_list(title, ep_json_list):
    db_id = []
    out_dir_list = []
    for filename in ep_json_list:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)["node"]
                episode_title = data['title']
                database_id = data['databaseId']
                subtitle = data['subtitle']
                accessibility = data['accessibility']
                if subtitle is None:
                    subtitle = ""
                out_dir = title+"/"+episode_title+subtitle
                out_dir = remove_illegal_characters(out_dir)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                http_img_dl(data['thumbnailUriTemplate'], out_dir+"/thumbnail.jpg")
                if accessibility == "READABLE":
                    db_id.append(database_id)
                    out_dir_list.append(out_dir)
    
    return db_id, out_dir_list

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
        