from typing import Tuple
import random, datetime, requests


def generate_random_date() -> str:

    start_date = datetime.date(1972, 6, 1)
    end_date = datetime.date(2021, 9, 22)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


def generate_random_date_range() -> Tuple[str, str]:

    first = generate_random_date()
    second = generate_random_date()
    while second < first:
        second = generate_random_date()
    
    return (first, second)


def simulate_increased_load():

    url = 'http://147.102.19.240/api/stock/show'

    for i in range(1000):
        f_date, s_date = generate_random_date_range()
        data = {
            's_Date' : str(f_date),
            'e_Date' : str(s_date)
        }
        requests.get(url, data=data)


simulate_increased_load()
