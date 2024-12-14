import os
import json
from http_req import http_post

def make_book_list(title, dir_list):
    db_id_list = []
    out_dir_list = []
    for out_dir_s in dir_list:
        filename = out_dir_s+"/book.json"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)["node"]
                book_title = data['title']
                accessibility = data['accessibility']
                db_id = data['databaseId']
                out_dir = title+"/"+book_title
                if accessibility == "READABLE":
                    db_id_list.append(db_id)
                    out_dir_list.append(out_dir)
    return db_id_list, out_dir_list

def getBookPages(db_id, needSave = False):
    url = "https://shonenjumpplus.com/api/v1/graphql?opname=VolumeViewer"

    payload = {
        "operationName":"VolumeViewer",
        "variables":{"volumeID":db_id},
        "query":"query VolumeViewer($volumeID: String!) { volume(databaseId: $volumeID) { __typename id ...CommonVolumeViewer pageImages { totalCount edges { node { src width height tshirtUrl kirinukiUrl clickableAreas { __typename ...ClickableArea } } } } packedImage { url } tableOfContents { title position { index } } previous { __typename id databaseId purchaseInfo { __typename ...PurchaseInfo } ...ViewerLink } next { __typename id databaseId purchaseInfo { __typename ...PurchaseInfo } ...ViewerLink } viewHistory { __typename ...RemoteViewHistory } ...VolumeImprintPage ...CommonReadableProductViewer } }  fragment SpineItem on Spine { readingDirection startPosition }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }  fragment CommonVolumeViewer on Volume { id databaseId publisherId title permalink number pageImageToken thumbnailUri spine { __typename ...SpineItem } openAt closeAt series { id databaseId mylisted volumeSeries { id databaseId publisherId title author { id databaseId name } } } purchaseInfo { __typename ...PurchaseInfo } }  fragment ClickableArea on Clickable { __typename appUrl position { __typename ... on PageIndexReadableProductPosition { pageIndex: index } ... on CFIReadableProductPosition { cfi } } ... on ClickableRect { height left top width } }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment ViewerLink on ReadableProduct { __typename id databaseId purchaseInfo { __typename ...PurchaseInfo } accessibility ... on Episode { publisherId } ... on Magazine { publisherId } ... on Volume { publisherId } ...AnalyticsParameters }  fragment RemoteViewHistory on ReadableProductViewHistory { lastViewedAt lastViewedPosition { __typename ... on PageIndexReadableProductPosition { index } } }  fragment ImprintPageNextContent on ReadableProduct { __typename id databaseId title thumbnailUriTemplate accessibility purchaseInfo { __typename ...PurchaseInfo } ... on Magazine { isSubscribersOnly } ...AnalyticsParameters }  fragment VolumeImprintPage on Volume { id databaseId next { __typename id databaseId series { id databaseId } ...ImprintPageNextContent } }  fragment EpisodeShareContent on Episode { id databaseId title shareUrl permalink series { id databaseId title } }  fragment ReadableProductShareContent on ReadableProduct { __typename id databaseId ... on Ebook { title shareUrl } ... on Episode { __typename ...EpisodeShareContent } ... on Magazine { title permalink shareUrl } ... on Volume { title permalink shareUrl } }  fragment CommonReadableProductViewer on ReadableProduct { __typename id databaseId accessibility purchaseInfo { __typename ...PurchaseInfo } ... on Episode { id databaseId pageImages { totalCount } } ... on Magazine { id databaseId pageImages { totalCount } } ... on Volume { id databaseId pageImages { totalCount } } ...ReadableProductShareContent ...AnalyticsParameters }"
    }

    response = http_post(url, payload)

    if needSave == False:
        return response

    pic_token = response.json()["data"]["volume"]["pageImageToken"]
    pics = response.json()["data"]["volume"]["pageImages"]["edges"]

    pic_src = []

    for i, edge in enumerate(pics):
        node = edge['node']
        url = node['src']

        pic_src.append(url)
    
    return pic_src, pic_token, response.json()