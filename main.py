import config
from getSeriesDetail import fetch_series_detail
from getSeriesDetailEpisodeList import fetch_series_detail_episode_list
import argparse
import json
from getEpisodeViewer import fetch_ep_viewer
from getDonwloadList import make_ep_list, getPages
from http_req import download_pic_src
from getBookList import fetch_book_list
from getBookDownloadList import make_book_list, getBookPages

def get_info(id):
    pass
    series_info = fetch_series_detail(id, show_info=True)

    ep_list = fetch_series_detail_episode_list(id, show_info=True)

    series = ep_list.get('data', {}).get('series', {})
    episodes = series.get('episodes', {}).get('edges', [])
    for index, edge in enumerate(episodes, start=1):
        pass
    

def download(id):
    title = fetch_series_detail(id, True, False)

    ep_json_list = fetch_series_detail_episode_list(id, title, True, False)
    db_id, out_dir_list = make_ep_list(title, ep_json_list)
    for ep in db_id:
        pic_url = getPages(ep)
        out_dir = out_dir_list[db_id.index(ep)]
        pic_token = fetch_ep_viewer(ep, out_dir, True, True)
        download_pic_src(pic_url, out_dir, pic_token)

    out_dir_list = fetch_book_list(id, title, True, False)
    #out_dir_list_1为去除不是readable之后的List
    db_id_list, out_dir_list_1 = make_book_list(title,out_dir_list)
    print(out_dir_list_1)
    for out_dir in out_dir_list_1:
        book_json = out_dir+"/book.json"
        db_id = db_id_list[out_dir_list_1.index(out_dir)]
        with open(book_json, 'r', encoding='utf-8') as file:
            book_json_data = json.load(file)
            db_id = book_json_data["node"]["databaseId"]
            pic_src, pic_token, response = getBookPages(db_id, True)
            download_pic_src(pic_src, out_dir, pic_token)
        with open(f"{out_dir}/volume_viewer.json", 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)



def main():
    config
    parser = argparse.ArgumentParser(description='A script to configure settings, get info, and download content.')
    
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    # Sub-command: reconfig
    parser_reconfig = subparsers.add_parser('reconfig', help='Reconfigure settings')

    # Sub-command: get-info
    parser_get_info = subparsers.add_parser('get-info', help='Get information by ID')
    parser_get_info.add_argument('id', type=str, help='ID to get information for')

    # Sub-command: download
    parser_download = subparsers.add_parser('download', help='Download content by ID')
    parser_download.add_argument('id', type=str, help='ID to download content for')

    args = parser.parse_args()

    if args.command == 'reconfig':   
        config.reconfig()
    elif args.command == 'get-info':
        get_info(args.id)
    elif args.command == 'download':
        download(args.id)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
