from http_req import http_post
import json
import os
from http_req import http_img_dl

def fetch_book_list(series_id, title="", needSave = False, show_info = False):
    url = "https://shonenjumpplus.com/api/v1/graphql?opname=BookList"

    payload = {
        "operationName":"BookList",
        "variables":{"seriesId":series_id,
        "offset":0,"sort":"NUMBER_ASC"},
        "query":"query BookList($seriesId: String!, $offset: Int = 0 , $first: Int = 99999 , $sort: ReadableProductSorting = NUMBER_ASC ) { series(databaseId: $seriesId) { volumeSeries { id databaseId publisherId title } id databaseId bulkPurchaseAvailable: hasPublicReadableProduct(type: VOLUME) readableProducts(first: $first, offset: $offset, sort: $sort, types: [EBOOK,VOLUME]) { pageInfo { __typename ...ForwardPageInfo } totalCount edges { node { __typename id databaseId ...BookListItem } } } hasVolume: hasPublicReadableProduct(type: VOLUME) } }  fragment ForwardPageInfo on PageInfo { hasNextPage endCursor }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }  fragment VolumeReadTrialAvailability on Volume { accessibility trialPageImages(first: 0) { totalCount } }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment BookListItem on ReadableProduct { __typename id publisherId databaseId title thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility ... on Volume { __typename description series { id databaseId } ...VolumeReadTrialAvailability } ... on Ebook { description series { id databaseId publisherId title } } ...AnalyticsParameters }"
    }

    response = http_post(url, payload)
    json_data = response.json()

    if show_info:
        return response.json()

    if needSave:
        out_dir_list = save_edges_to_json(json_data, title)
        with open(f"{title}/books.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return out_dir_list
    
def save_edges_to_json(json_data, title):
    out_dir_list = []
    # 解析JSON数据
    series = json_data.get('data', {}).get('series', {})
    episodes = series.get('readableProducts', {}).get('edges', [])
    
    # 遍历edges项目
    for index, edge in enumerate(episodes, start=1):
        # 构建新JSON文件名
        book_title = edge['node']['title']
        out_dir = title+"/"+book_title
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        filename = os.path.join(out_dir, f'book.json')

        out_dir_list.append(out_dir)

        thumbnail_url = edge['node']['thumbnailUriTemplate']
        http_img_dl(thumbnail_url, out_dir+"/thumbnail.png")
        
        # 保存当前edge到新JSON文件
        with open(filename, 'w') as f:
            json.dump(edge, f, indent=4)
    return out_dir_list