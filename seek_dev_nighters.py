import requests
import datetime
from datetime import datetime
from datetime import timezone


def get_accounts(link_api):
    response = requests.get(link_api)
    if not response.ok:
        return None
    response_accounts = response.json()
    return response_accounts


def get_format_time(account):
    time_stamp = account['timestamp']
    loc_time = datetime.fromtimestamp(time_stamp, tz=timezone.utc)
    return loc_time


def get_midnight_attempts(midnight_attempts):
    posts_list = []
    for account in midnight_attempts:
        time_account = get_format_time(account)
        if 0 < time_account.hour < 5:
            posts_list.append(account)
    return posts_list


def load_attempts(link_api, accounts_json):
    page = 0
    while page != accounts_json['number_of_pages']:
        page = page + 1
        payload = (('page', page),)
        accounts_page = requests.get(link_api, params=payload)
        midnight_attempts = accounts_page.json()['records']
        midnight_attempts = get_midnight_attempts(midnight_attempts)
        if midnight_attempts:
            yield midnight_attempts


def output_midnighters(midnight_attempt):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    for account in midnight_attempt:
        time_posted = get_format_time(account).strftime(fmt)
        path_file_out = 'username:{username} total time_posted:{time_posted}'.\
            format(username=account['username'], time_posted=time_posted)
        print('midnight_attempt account: ', path_file_out)
        break


def main():
    link = 'http://devman.org/api/challenges/solution_attempts'
    accounts = get_accounts(link)
    if accounts is None:
        exit('not correct link')
    for midnight_attempt in load_attempts(link, accounts):
        output_midnighters(midnight_attempt)


if __name__ == '__main__':
    main()
