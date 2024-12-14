from turtle import title
import json
import os
from http_req import http_post
from http_req import http_img_dl
        
#读取漫画列表

def fetch_series_detail_episode_list(series_id, title = "", needSave = False, show_info = False):
    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=SeriesDetailEpisodeList'

    ep_response = get_episode_count(series_id)
    totalCount = ep_response.json()["data"]["series"]["episodes"]["totalCount"]

    payload = {
        "operationName": "SeriesDetailEpisodeList",
        "variables": {"id": series_id, "episodeOffset": 0,  "episodeFirst": totalCount},
        "query": "query SeriesDetailEpisodeList($id: String!, $episodeOffset: Int = 0 , $episodeFirst: Int = 100 , $episodeSort: ReadableProductSorting = null ) { series(databaseId: $id) { __typename id databaseId episodeDefaultSorting episodes: readableProducts(types: [EPISODE,SPECIAL_CONTENT], first: $episodeFirst, offset: $episodeOffset, sort: $episodeSort) { totalCount pageInfo { __typename ...ForwardPageInfo } edges { node { __typename id databaseId ...EpisodeListItem ...SpecialContentListItem } } } ...SeriesDetailBottomBanners } }  fragment ForwardPageInfo on PageInfo { hasNextPage endCursor }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }  fragment EpisodeIsViewed on Episode { id databaseId isViewed }  fragment EpisodeListItem on Episode { __typename id databaseId publisherId title subtitle thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt isSakiyomi completeReadingInfo { visitorCanGetPoint gettablePoint } viewCount series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } ...EpisodeIsViewed }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment SpecialContentListItem on SpecialContent { __typename id databaseId publisherId title thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt linkUrl series { id databaseId publisherId title serialUpdateScheduleLabel } ...AnalyticsParameters }  fragment SeriesDetailBottomBanners on Series { id databaseId bannerGroup(groupName: \"series_detail_bottom\") { __typename ... on ImageBanner { databaseId imageUriTemplate imageUrl linkUrl } ... on YouTubeBanner { videoId } } }"
    }

    response = http_post(url, payload)
    json_data = response.json()

    if show_info:
        return response.json()

    if needSave:

        ep_json_list = save_edges_to_json(json_data, title)
        with open(f"{title}/episode.json", "w", encoding="utf-8") as f:
            json.dump(ep_response.json(), f, ensure_ascii=False, indent=4)

        bannerGroup = json_data.get('data', {}).get('series', {}).get('bannerGroup', {})
        for index, banner in enumerate(bannerGroup, start=1):
            image_url = banner.get('imageUrl')
            if image_url:
                http_img_dl(image_url, f"{title}/banner_{index}.png")
        return ep_json_list


def get_episode_count(series_id):
    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=SeriesDetailEpisodeList'
    payload = {
        "operationName": "SeriesDetailEpisodeList",
        "variables": {"id": series_id, "episodeOffset": -1,  "episodeFirst": 0},
        "query": "query SeriesDetailEpisodeList($id: String!, $episodeOffset: Int = 0 , $episodeFirst: Int = 100 , $episodeSort: ReadableProductSorting = null ) { series(databaseId: $id) { __typename id databaseId episodeDefaultSorting episodes: readableProducts(types: [EPISODE,SPECIAL_CONTENT], first: $episodeFirst, offset: $episodeOffset, sort: $episodeSort) { totalCount pageInfo { __typename ...ForwardPageInfo } edges { node { __typename id databaseId ...EpisodeListItem ...SpecialContentListItem } } } ...SeriesDetailBottomBanners } }  fragment ForwardPageInfo on PageInfo { hasNextPage endCursor }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }  fragment EpisodeIsViewed on Episode { id databaseId isViewed }  fragment EpisodeListItem on Episode { __typename id databaseId publisherId title subtitle thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt isSakiyomi completeReadingInfo { visitorCanGetPoint gettablePoint } viewCount series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } ...EpisodeIsViewed }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment SpecialContentListItem on SpecialContent { __typename id databaseId publisherId title thumbnailUriTemplate purchaseInfo { __typename ...PurchaseInfo } accessibility publishedAt linkUrl series { id databaseId publisherId title serialUpdateScheduleLabel } ...AnalyticsParameters }  fragment SeriesDetailBottomBanners on Series { id databaseId bannerGroup(groupName: \"series_detail_bottom\") { __typename ... on ImageBanner { databaseId imageUriTemplate imageUrl linkUrl } ... on YouTubeBanner { videoId } } }"
    }

    response = http_post(url, payload)

    return response

def save_edges_to_json(json_data, title):
    ep_json_list = []
    # 解析JSON数据
    series = json_data.get('data', {}).get('series', {})
    episodes = series.get('episodes', {}).get('edges', [])
    
    # 遍历edges项目
    for index, edge in enumerate(episodes, start=1):
        # 构建新JSON文件名
        episode_title = edge['node']['title']
        subtitle = edge['node']['subtitle']
        if subtitle is None:
            subtitle = ""
        out_dir = title+"/"+episode_title+subtitle
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        filename = os.path.join(out_dir, f'episode_{index}.json')

        ep_json_list.append(filename)
        
        # 保存当前edge到新JSON文件
        with open(filename, 'w') as f:
            json.dump(edge, f, indent=4)
    return ep_json_list