import json
import os
from http_req import http_post,http_img_dl
        
#从任意地方点击进详细页
#请求方法POST
#请求需要头authorization
#请求体见下payload

def fetch_series_detail(series_id, needSave = False, show_info = False):
    url = 'https://shonenjumpplus.com/api/v1/graphql?opname=SeriesDetail'
    
    payload = {
        "operationName": "SeriesDetail",
        "variables": {"id": series_id},
        "query": "query SeriesDetail($id: String!) { series(databaseId: $id) { __typename id databaseId ...SeriesDetailHeader serialUpdateScheduleLabel jamEpisodeWorkType openAt latestBook: readableProducts(types: [VOLUME,EBOOK], first: 1, sort: NUMBER_DESC) { edges { node { __typename id databaseId ...BookVolumeDetailHeader } } } volumeAppeal { isAdvanceNotice text } firstEpisode { id databaseId title } volumeSeries { id publisherId title } hasEpisode: hasPublicReadableProduct(type: EPISODE) hasVolume: hasPublicReadableProduct(type: VOLUME) hasEbook: hasPublicReadableProduct(type: EBOOK) hasSpecialContent: hasPublicReadableProduct(type: SPECIAL_CONTENT) } }  fragment SubThumbnail on ThumbnailImage { uriTemplate width height }  fragment SerialInfoIcon on SerialInfo { isOriginal isIndies }  fragment SeriesShareContent on Series { id databaseId publisherId title shareUrl serialUpdateScheduleLabel openAt seriesAuthor: author { id databaseId name } firstEpisode { id databaseId permalink } }  fragment SeriesDetailHeader on Series { __typename id databaseId thumbnailUriTemplate horizontalThumbnail: subThumbnail(type: HORIZONTAL_WITHOUT_LOGO) { __typename ...SubThumbnail } supportsOnetimeFree serialInfo { __typename ...SerialInfoIcon status } serialUpdateScheduleLabel totalViewCount mylistedCount title seriesAuthor: author { id databaseId name } underThumbnailBannerGroup: bannerGroup(groupName: \"series_detail_under_thumbnail\") { __typename ... on TextBanner { databaseId text } } headerBannerGroup: bannerGroup(groupName: \"series_detail_top\") { __typename ... on TextBanner { databaseId text linkUrl } ... on ImageBanner { databaseId imageUriTemplate imageUrl linkUrl alt } ... on YouTubeBanner { videoId } } ...SeriesShareContent }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment BookVolumeDetailHeader on ReadableProduct { __typename id databaseId publisherId title thumbnailUriTemplate ... on Ebook { authorName series { id databaseId publisherId seriesAuthor: author { id databaseId name } } } ... on Volume { authorName series { id databaseId seriesAuthor: author { id databaseId name } } } ...AnalyticsParameters }"
    }

    response = http_post(url, payload)
    
    series = response.json()["data"]["series"]
    
    title = series["title"]
    typename = series["__typename"]
    jam_episode_work_type = series["jamEpisodeWorkType"]

    has_Ebook = series["hasEbook"]
    has_episode = series["hasEpisode"]
    has_volume = series["hasVolume"]
    hasSpecialContent = series["hasSpecialContent"]
    supports_onetime_free = series["supportsOnetimeFree"]

    openAt = series["openAt"]
    serial_update_schedule_label = series["serialUpdateScheduleLabel"]

    databaseId = series["databaseId"]
    publisherId = series["publisherId"]

    mylistedCount = series["mylistedCount"]
    totalViewCount = series["totalViewCount"]

    #推荐语
    isAdvanceNotice = series["volumeAppeal"]["isAdvanceNotice"]
    volumeAppealText = series["volumeAppeal"]["text"]

    #作者
    series_author = series["seriesAuthor"]["name"]

    #系列情况SerialInfo
    isIndies = series["serialInfo"]["isIndies"]
    isOriginal = series["serialInfo"]["isOriginal"]
    status = series["serialInfo"]["status"]

    #头图
    horizontalThumbnail = series["horizontalThumbnail"]
    horizontalThumbnail_url = horizontalThumbnail["uriTemplate"]
    horizontalThumbnail_width = horizontalThumbnail["width"]
    horizontalThumbnail_height = horizontalThumbnail["height"]

    #缩略图
    thumbnailUriTemplate = series["thumbnailUriTemplate"]

    horizontalThumbnail_url = horizontalThumbnail_url.replace("{width}", str(horizontalThumbnail_width))
    thumbnailUriTemplate = thumbnailUriTemplate.replace("{width}", "999999999")
    
    if show_info:
        return response.json()
    
    if needSave:
        if not os.path.exists(title):
            os.makedirs(title)
        http_img_dl(horizontalThumbnail_url, f"{title}/horizontal_thumbnail.jpg")
        http_img_dl(thumbnailUriTemplate, f"{title}/thumbnail.jpg")
        with open(f"{title}/series.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)

        with open(f"{title}/series_info.json", "w", encoding="utf-8") as f:
            json.dump(fetch_series_info(series_id).json(), f, ensure_ascii=False, indent=4)

    return title

def fetch_series_info(series_id):
    url = "https://shonenjumpplus.com/api/v1/graphql?opname=SeriesDetailSeriesInfo"

    payload = {
        "operationName":"SeriesDetailSeriesInfo",
        "variables":{"id":series_id},
        "query":"query SeriesDetailSeriesInfo($id: String!) { series(databaseId: $id) { __typename id databaseId ...SeriesDetailInfo } }  fragment SeriesAuthors on Series { authors { id databaseId name } }  fragment PurchaseInfo on PurchaseInfo { isFree hasPurchased hasPurchasedViaTicket purchasable purchasableViaTicket purchasableViaPaidPoint purchasableViaOnetimeFree unitPrice rentable rentalEndAt hasRented rentableByPaidPointOnly rentalTermMin }  fragment FreeSerialEpisodeItem on Episode { id databaseId title thumbnailUriTemplate publishedAt purchaseInfo { __typename ...PurchaseInfo } accessibility }  fragment AnalyticsParameters on ReadableProduct { __typename id databaseId publisherId title ... on Episode { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } ... on Volume { openAt series { id databaseId publisherId title } } ... on Ebook { publishedAt series { id databaseId publisherId title } } ... on Magazine { openAt magazineLabel { id databaseId publisherId title } } ... on SpecialContent { publishedAt series { id databaseId publisherId title serialUpdateScheduleLabel jamEpisodeWorkType } } }  fragment SerialInfoIcon on SerialInfo { isOriginal isIndies }  fragment HorizontalRecommendedSeriesItem on Series { id databaseId publisherId title thumbnailUriTemplate readableProducts(first: 1, sort: NUMBER_DESC, types: [VOLUME,EBOOK]) { edges { node { id databaseId thumbnailUriTemplate } } } volumeSeries { id databaseId publisherId title } hasEpisode: hasPublicReadableProduct(type: EPISODE) hasEbook: hasPublicReadableProduct(type: EBOOK) hasVolume: hasPublicReadableProduct(type: VOLUME) hasSpecialContent: hasPublicReadableProduct(type: SPECIAL_CONTENT) serialInfo { __typename ...SerialInfoIcon status } supportsOnetimeFree }  fragment SeriesDetailBottomBanners on Series { id databaseId bannerGroup(groupName: \"series_detail_bottom\") { __typename ... on ImageBanner { databaseId imageUriTemplate imageUrl linkUrl } ... on YouTubeBanner { videoId } } }  fragment SeriesShareContent on Series { id databaseId publisherId title shareUrl serialUpdateScheduleLabel openAt seriesAuthor: author { id databaseId name } firstEpisode { id databaseId permalink } }  fragment SeriesDetailInfo on Series { __typename id databaseId publisherId shortDescription description ...SeriesAuthors freeSerialEpisodes { __typename id databaseId ...FreeSerialEpisodeItem ...AnalyticsParameters } mainGenre { id name series(first: 11, sort: SHUFFLE) { edges { node { __typename id databaseId ...HorizontalRecommendedSeriesItem } } } } ...SeriesDetailBottomBanners ...SeriesShareContent recommendedSeriesByAuthor: recommendedSeriesByType(type: SERIES_BY_AUTHOR) { __typename id databaseId ...HorizontalRecommendedSeriesItem } }"
    }

    return http_post(url, payload)