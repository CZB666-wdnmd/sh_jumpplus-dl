from turtle import title
import requests
import json
import os
import config

def save_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        response.raise_for_status()
        
def fetch_series_detail_episode_list(series_id, title):
    authorization = config.authorization
    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=SeriesDetailEpisodeList'
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
        "operationName": "SeriesDetailEpisodeList",
        "variables": {"id": series_id, "episodeOffset": -1,  "episodeFirst": 0},
        "query": "query SeriesDetailEpisodeList($id: String!, $episodeOffset: Int = 0 , $episodeFirst: Int = 100 , $episodeSort: ReadableProductSorting = null ) { series(databaseId: $id) { __typename id databaseId episodeDefaultSorting episodes: readableProducts(types: [EPISODE,SPECIAL_CONTENT], first: $episodeFirst, offset: $episodeOffset, sort: $episodeSort) { totalCount pageInfo { __typename ...ForwardPageInfo } edges { node { __typename id databaseId ...EpisodeListItem ...SpecialContentListItem } } } ...SeriesDetailBottomBanners } }  fragment ForwardPageInfo on PageInfo { hasNextPage endCursor }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }  fragment EpisodeIsViewed on Episode { id databaseId isViewed }  fragment EpisodeListItem on Episode { __typename id databaseId publisherId title subtitle thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt isSakiyomi completeReadingInfo { visitorCanGetPoint gettablePoint } viewCount series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } ...EpisodeIsViewed }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment SpecialContentListItem on SpecialContent { __typename id databaseId publisherId title thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt linkUrl series { id databaseId publisherId title serialUpdateScheduleLabel } ...AnalyticsParameters }  fragment SeriesDetailBottomBanners on Series { id databaseId bannerGroup(groupName: \"series_detail_bottom\") { __typename ... on ImageBanner { databaseId imageUriTemplate imageUrl linkUrl } ... on YouTubeBanner { videoId } } }"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    totalCount = response.json()["data"]["series"]["episodes"]["totalCount"]

    payload = {
        "operationName": "SeriesDetailEpisodeList",
        "variables": {"id": series_id, "episodeOffset": 0,  "episodeFirst": totalCount, "episodeSort": "NUMBER_ASC"},
        "query": "query SeriesDetailEpisodeList($id: String!, $episodeOffset: Int = 0 , $episodeFirst: Int = 100 , $episodeSort: ReadableProductSorting = null ) { series(databaseId: $id) { __typename id databaseId episodeDefaultSorting episodes: readableProducts(types: [EPISODE,SPECIAL_CONTENT], first: $episodeFirst, offset: $episodeOffset, sort: $episodeSort) { totalCount pageInfo { __typename ...ForwardPageInfo } edges { node { __typename id databaseId ...EpisodeListItem ...SpecialContentListItem } } } ...SeriesDetailBottomBanners } }  fragment ForwardPageInfo on PageInfo { hasNextPage endCursor }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }  fragment EpisodeIsViewed on Episode { id databaseId isViewed }  fragment EpisodeListItem on Episode { __typename id databaseId publisherId title subtitle thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt isSakiyomi completeReadingInfo { visitorCanGetPoint gettablePoint } viewCount series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } ...EpisodeIsViewed }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment SpecialContentListItem on SpecialContent { __typename id databaseId publisherId title thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt linkUrl series { id databaseId publisherId title serialUpdateScheduleLabel } ...AnalyticsParameters }  fragment SeriesDetailBottomBanners on Series { id databaseId bannerGroup(groupName: \"series_detail_bottom\") { __typename ... on ImageBanner { databaseId imageUriTemplate imageUrl linkUrl } ... on YouTubeBanner { videoId } } }"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    json_data = response.json()
    save_edges_to_json(json_data, title)

def save_edges_to_json(json_data, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 解析JSON数据
    series = json_data.get('data', {}).get('series', {})
    episodes = series.get('episodes', {}).get('edges', [])
    
    # 遍历edges项目
    for index, edge in enumerate(episodes, start=1):
        # 构建新JSON文件名
        filename = os.path.join(output_dir, f'episode_{index}.json')
        
        # 保存当前edge到新JSON文件
        with open(filename, 'w') as f:
            json.dump(edge, f, indent=4)
