import config
from getSeriesDetail import fetch_series_detail
from getSeriesDetailEpisodeList import fetch_series_detail_episode_list
from download_manga_json import download_all
from download_manga_json import download_one
import argparse

def config_settings():
    config.reconfig

def get_info(id):
    title = fetch_series_detail(id)

def download(id, range=None):
    title = fetch_series_detail(id)
    fetch_series_detail_episode_list(id, title)
    if range:
        download_one(ep, title)
    else:
        download_all(title)

def main():
    config
    parser = argparse.ArgumentParser(description='A script to configure settings, get info, and download content.')
    
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    # Sub-command: config
    parser_config = subparsers.add_parser('config', help='Configure settings')

    # Sub-command: get-info
    parser_get_info = subparsers.add_parser('get-info', help='Get information by ID')
    parser_get_info.add_argument('id', type=str, help='ID to get information for')

    # Sub-command: download
    parser_download = subparsers.add_parser('download', help='Download content by ID')
    parser_download.add_argument('id', type=str, help='ID to download content for')
    parser_download.add_argument('-e', '--range', type=str, help='Range of content to download')

    args = parser.parse_args()

    if args.command == 'config':
        config_settings()
    elif args.command == 'get-info':
        get_info(args.id)
    elif args.command == 'download':
        download(args.id, args.range)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
