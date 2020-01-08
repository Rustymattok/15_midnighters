import pytz
import requests
from datetime import datetime


def get_local_time(time_stamp, time_zone):
    loc_time = datetime.fromtimestamp(time_stamp, tz=pytz.timezone(time_zone))
    return loc_time


def get_midnight_attempts(attempts):
    midnight_attempts = []
    for attempt in attempts:
        time_account = get_local_time(
            attempt['timestamp'], attempt['timezone']
        )
        if 0 < time_account.hour < 5:
            midnight_attempts.append(attempt)
    return midnight_attempts


def load_attempts(link_api):
    page = 0
    while True:
        page = page + 1
        payload = {'page': page}
        accounts_page = requests.get(link_api, params=payload)
        if not accounts_page.ok:
            return False
        attempts = accounts_page.json()['records']
        midnight_attempts = get_midnight_attempts(attempts)
        yield from midnight_attempts


def get_users_attempts(midnight_attempts):
    user_attempts = dict()
    key_time = 0
    for midnight_attempt in midnight_attempts:
        if midnight_attempt['username'] in user_attempts.keys():
            user_attempts[midnight_attempt['username']][key_time].\
                append(str(midnight_attempt['timestamp']))
        else:
            user_attempts[midnight_attempt['username']] = [
                [str(midnight_attempt['timestamp'])],
                str(midnight_attempt['timezone'])
            ]
    return user_attempts


def output_midnighters(midnight_attempts):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    user_attempts = get_users_attempts(midnight_attempts)
    key_time = 0
    key_time_zone = 1
    for user_name in user_attempts:
        print('midnight_attempt account: ', user_name)
        for time_attempt in user_attempts[user_name][key_time]:
            time_zone = user_attempts[user_name][key_time_zone]
            time_posted = get_local_time(float(time_attempt), time_zone).\
                strftime(fmt)
            path_file_out = 'total time_posted:{time_posted}'. \
                format(time_posted=time_posted)
            print(path_file_out)


def main():
    link = 'http://devman.org/api/challenges/solution_attempts'
    if not requests.get(link).ok:
        print('not correct link')
    output_midnighters(load_attempts(link))


if __name__ == '__main__':
    main()
