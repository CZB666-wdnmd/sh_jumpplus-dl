import config
from getSeriesDetail import fetch_series_detail
from getSeriesDetailEpisodeList import fetch_series_detail_episode_list
from download_manga_json import download_all
from download_manga_json import download_one


def main():
    config
    series_id = input("Enter the series ID: ")
    title = fetch_series_detail(series_id)

    fetch_series_detail_episode_list(series_id, title)

    user_unput = input("Download now? ALL or enter number you want")

    if 1:
        print("go to dl !")
        download_all(title)
    else:
        dl_list = user_unput.split()
        for ep in dl_list:
            download_one(ep, title)
    
if __name__ == "__main__":
    main()
