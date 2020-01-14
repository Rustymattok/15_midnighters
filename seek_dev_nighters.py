import pytz
import requests
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
    if 0 < time_account.hour < 5 and not None:
        return True
    return False


def load_attempts(link_api):
    page = 0
    number_of_pages = requests.get(link_api).json()['number_of_pages']
    while True:
        page = page + 1
        if page > number_of_pages:
            return False
        payload = {'page': page}
        accounts_page = requests.get(link_api, params=payload)
        attempts = accounts_page.json()['records']
        midnight_attempts = get_midnight_attempts(attempts)
        yield from midnight_attempts


def get_users_attempts(midnight_attempts):
    user_attempts = defaultdict(list)
    for midnight_attempt in midnight_attempts:
        user_attempts[midnight_attempt['username']].append(
            (midnight_attempt['timezone'], midnight_attempt['timestamp'])
        )
    return user_attempts


def output_midnighters(midnight_attempts):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    user_attempts = get_users_attempts(midnight_attempts)
    key_username = 0
    key_time = 1
    for user in user_attempts.items():
        print('midnight_attempt account: ', user[key_username])
        for time_zone, time_stamp in user[key_time]:
            time_posted = get_local_time(time_stamp, time_zone).strftime(fmt)
            out_put_time = 'total time_posted:{time_posted}'.\
                format(time_posted=time_posted)
            print(out_put_time)


def main():
    link = 'http://devman.org/api/challenges/solution_attempts'
    if not requests.get(link).ok:
        print('not correct link')
    try:
        output_midnighters(get_midnight_attempts(load_attempts(link)))
    except ValueError:
        print('no json data')


if __name__ == '__main__':
    main()
