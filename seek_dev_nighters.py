import pytz
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from collections import defaultdict


def get_local_time(time_stamp, time_zone):
    loc_time = datetime.fromtimestamp(time_stamp, tz=pytz.timezone(time_zone))
    return loc_time


def get_midnight_attempts(attempts):
    midnight_attempts = []
    for attempt in attempts:
        if is_midnight_attempt(attempt):
            midnight_attempts.append(attempt)
    return midnight_attempts


def is_midnight_attempt(attempt):
    time_account = get_local_time(attempt['timestamp'], attempt['timezone'])
    return 0 < time_account.hour < 5


def load_attempts(link_api):
    page = 0
    while True:
        page = page + 1
        payload = {'page': page}
        try:
            accounts_page = requests.get(link_api, params=payload)
            accounts_page.raise_for_status()
            attempts = accounts_page.json()['records']
            yield from attempts
        except HTTPError:
            return False


def count_users_attempts(midnight_attempts):
    user_attempts = defaultdict(list)
    for midnight_attempt in midnight_attempts:
        user_attempts[midnight_attempt['username']].append(
            (midnight_attempt['timezone'], midnight_attempt['timestamp'])
        )
    return user_attempts


def get_output_time(time_stamp, time_zone):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    time_posted = get_local_time(time_stamp, time_zone).strftime(fmt)
    out_put_time = 'total time_posted:{time_posted}'.\
        format(time_posted=time_posted)
    return out_put_time


def output_midnighters(midnight_attempts):
    user_attempts = count_users_attempts(midnight_attempts)
    key_username = 0
    key_time = 1
    for user in user_attempts.items():
        print('midnight_attempt account: ', user[key_username])
        for time_zone, time_stamp in user[key_time]:
            print(get_output_time(time_stamp, time_zone))


def main():
    link = 'http://devman.org/api/challenges/solution_attempts'
    if not requests.get(link).ok:
        print('not correct link')
    try:
        output_midnighters(get_midnight_attempts(load_attempts(link)))
    except HTTPError:
        print('error link')


if __name__ == '__main__':
    main()
