import argparse
import requests
import pytz
import datetime
from datetime import datetime
import os
from requests.exceptions import MissingSchema


def get_accounts_json(link_api):
    response = requests.get(link_api)
    if response.status_code == 404:
        return None
    resp_json = response.json()
    return resp_json


def get_number_pages(accounts_json):
    number_pages = accounts_json['number_of_pages']
    return number_pages


def get_format_time(account):
    time_zone = account['timezone']
    time_stamp = account['timestamp']
    eastern = pytz.timezone(time_zone)
    loc_time = eastern.localize(datetime.utcfromtimestamp(time_stamp))
    return loc_time


def get_late_posts(accounts_list):
    posts_list = []
    for account in accounts_list:
        time_account = get_format_time(account)
        if 0 < time_account.hour < 5:
            posts_list.append(account)
    return posts_list


def load_attempts(link_api, number_pages):
    link_pages = os.path.join(link_api, '?page=')
    posted_late_list = []
    for page in range(1, number_pages + 1):
        link_page = link_pages + str(page)
        accounts_list = get_accounts_json(link_page)['records']
        list_to_add = get_late_posts(accounts_list)
        if list_to_add:
            posted_late_list = posted_late_list + list_to_add
    return posted_late_list


def output_midnighters(accounts_list):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    for account in accounts_list:
        time_posted = get_format_time(account).strftime(fmt)
        path_file_out = 'username:{username} total time_posted:{time_posted}'.\
            format(username=account['username'], time_posted=time_posted)
        print(path_file_out)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l',
        '--link',
        required=False,
        type=str,
        default='http://devman.org/api/challenges/solution_attempts',
        help='command - file path for re-size'
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    pars_link = args.link
    accounts_json = get_accounts_json(pars_link)
    if accounts_json is None:
        exit('not correct link')
    number_page = get_number_pages(accounts_json)
    accounts_late_posted = load_attempts(pars_link, number_page)
    output_midnighters(accounts_late_posted)


if __name__ == '__main__':
    main()
