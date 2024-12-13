import config
from getSeriesDetail import fetch_series_detail
from getSeriesDetailEpisodeList import fetch_series_detail_episode_list
import argparse
import json
from getEpisodeViewer import fetch_ep_viewer
from getDonwloadList import make_ep_list, getPages
from http_req import download_pic_src

def get_info(id):
    series_info = fetch_series_detail(id, show_info=True)

    ep_list = fetch_series_detail_episode_list(id, show_info=True)

    series = ep_list.get('data', {}).get('series', {})
    episodes = series.get('episodes', {}).get('edges', [])
    for index, edge in enumerate(episodes, start=1):
        pass
    

def download(id):
    title = fetch_series_detail(id, True, False)
    fetch_series_detail_episode_list(id, title, True, False)
    db_id, out_dir_list = make_ep_list(title)
    for ep in db_id:
        pic_url = getPages(ep)
        out_dir = out_dir_list[db_id.index(ep)]
        pic_token = fetch_ep_viewer(ep, out_dir, True, True)
        download_pic_src(pic_url, out_dir, pic_token)



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
