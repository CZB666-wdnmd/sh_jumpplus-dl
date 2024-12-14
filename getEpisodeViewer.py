import json
import os
from http_req import http_post

#获取漫画token方法 get_token(ep_id, req_token = True)

def fetch_ep_viewer(ep_id, save_path="", need_save = False, req_token = False):
    url = "https://shonenjumpplus.com/api/v1/graphql?opname=EpisodeViewer"

    payload = {
        "operationName":"EpisodeViewer",
        "variables":{"episodeID":ep_id},
        "query":"query EpisodeViewer($episodeID: String!) { episode(databaseId: $episodeID) { id databaseId publisherId title number publishedAt pageImageToken spine { readingDirection startPosition } previousSpecialContent { id databaseId linkUrl } nextSpecialContent { id databaseId linkUrl } series { id databaseId publisherId title author { id databaseId name } serialUpdateScheduleLabel jamEpisodeWorkType openAt } } stampCard { __typename ...StampCardIcon } }  fragment StampCardIcon on StampCard { id databaseId iconImageUrl }"
    }
    
    response = http_post(url, payload)
    
    if need_save:
        filename = response.json()["data"]["episode"]["title"]
        with open(os.path.join(save_path, f"{filename}_ep_viewer.json"), "w") as f:
            json.dump(response.json(), f, indent=4)
            
    if req_token:
        return response.json()["data"]["episode"]["pageImageToken"]
