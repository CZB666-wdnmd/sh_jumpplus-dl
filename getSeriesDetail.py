import json
import os
from http_req import http_post,http_img_dl
        
def fetch_series_detail(series_id):
    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=SeriesDetail'
    
    payload = {
        "operationName": "SeriesDetail",
        "variables": {"id": series_id},
        "query": "query SeriesDetail($id: String!) { series(databaseId: $id) { __typename id databaseId ...SeriesDetailHeader serialUpdateScheduleLabel jamEpisodeWorkType openAt latestVolume: readableProducts(types: [VOLUME], first: 1, sort: NUMBER_DESC) { edges { node { __typename id databaseId ...BookVolumeDetailHeader } } } volumeAppeal { isAdvanceNotice text } firstEpisode { id databaseId title } volumeSeries { id publisherId title } hasEpisode: hasPublicReadableProduct(type: EPISODE) hasVolume: hasPublicReadableProduct(type: VOLUME) } } fragment SubThumbnail on ThumbnailImage { uriTemplate width height } fragment SerialInfoIcon on SerialInfo { isOriginal isIndies } fragment SeriesShareContent on Series { id databaseId publisherId title shareUrl serialUpdateScheduleLabel openAt seriesAuthor: author { id databaseId name } firstEpisode { id databaseId permalink } } fragment SeriesDetailHeader on Series { __typename id databaseId thumbnailUriTemplate horizontalThumbnail: subThumbnail(type: HORIZONTAL_WITHOUT_LOGO) { __typename ...SubThumbnail } supportsOnetimeFree serialInfo { __typename ...SerialInfoIcon status } serialUpdateScheduleLabel totalViewCount title seriesAuthor: author { id databaseId name } underThumbnailBannerGroup: bannerGroup(groupName: \"series_detail_under_thumbnail\") { __typename ... on TextBanner { databaseId text } } headerBannerGroup: bannerGroup(groupName: \"series_detail_top\") { __typename ... on TextBanner { databaseId text linkUrl } ... on ImageBanner { databaseId imageUriTemplate imageUrl linkUrl alt } ... on YouTubeBanner { videoId } } ...SeriesShareContent } fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } } fragment BookVolumeDetailHeader on ReadableProduct { __typename id databaseId publisherId title thumbnailUriTemplate ... on Ebook { authorName series { id databaseId publisherId seriesAuthor: author { id databaseId name } } } ... on Volume { authorName series { id databaseId seriesAuthor: author { id databaseId name } } } ...AnalyticsParameters }"
    }

    response = http_post(url, payload)
        
    series = response.json()["data"]["series"]
    
    title = series["title"]
    typename = series["__typename"]
    jam_episode_work_type = series["jamEpisodeWorkType"]
    database_id = series["databaseId"]
    publisher_id = series["publisherId"]
    has_episode = series["hasEpisode"]
    has_volume = series["hasVolume"]
    volume_others = series["volumeAppeal"]['text']
    open_at = series["openAt"]
    serial_update_schedule_label = series["serialUpdateScheduleLabel"]
    series_author = series["seriesAuthor"]["name"]
    supports_onetime_free = series["supportsOnetimeFree"]
    is_Indeis = series["serialInfo"]["isIndies"]
    is_Original = series["serialInfo"]["isOriginal"]
    
    print(f"名：{title}")
    print(f"类型：{typename}    {jam_episode_work_type}")
    print(f"数据库ID：{database_id}")
    print(f"公开ID：{publisher_id}")
    print(f"分集：{has_episode}")
    print(f"单行本：{has_volume}")
    print(f"单行本其他信息：{volume_others}")
    print(f"开始连载：{open_at}")
    print(f"更新计划：{serial_update_schedule_label}")
    print(f"作者：{series_author}")
    print(f"初回免费：{supports_onetime_free}")
    print(f"独立制作：{is_Indeis}")
    print(f"原创制作：{is_Original}")

    # Create directory for the series
    if not os.path.exists(title):
        os.makedirs(title)

    # Download and save images
    horizontal_thumbnail = series["horizontalThumbnail"]["uriTemplate"]
    horizontal_url = horizontal_thumbnail.format(height=1000000000000, width=10000000000000)
    http_img_dl(horizontal_url, os.path.join(title, "ThumbnailImage.png"))

    thumbnail_uri_template = series["thumbnailUriTemplate"]
    thumbnail_url = thumbnail_uri_template.format(height=100000, width=100000)
    http_img_dl(thumbnail_url, os.path.join(title, "ThumbnailImage_little.png"))

