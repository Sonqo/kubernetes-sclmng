from typing import Tuple
import random, datetime, requests


def generate_random_date() -> str:

    start_date = datetime.date(2020, 8, 1)
    end_date = datetime.date(2020, 10, 31)

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

    url = 'http://35.205.254.108/api/api/ride/show'

    hour = random.randint(10, 23)

    for i in range(1000):
        f_date, _ = generate_random_date_range()
        data = {
            's_Date' : str(f_date) + ' {}:00:00'.format(hour),
            'e_Date' : str(f_date) + ' {}:00:00'.format(hour+2)
        }
        res = requests.get(url, data=data)
        print('Requests made: {} | Execution time: {}'.format(i, res.elapsed.total_seconds()))

simulate_increased_load()
