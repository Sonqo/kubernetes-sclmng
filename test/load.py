import pandas as pd
import seaborn as sns
from typing import Tuple
import random, datetime, requests
import matplotlib.pyplot as plt

def reshome(url, data, latency):
    try:
        reshomee = requests.get(url, data=data, timeout=10)
        return reshomee.elapsed.total_seconds() + latency
    except requests.exceptions.Timeout:
        return reshome(url, data, 10)

def generate_random_date() -> str:

    start_date = datetime.date(2020, 10, 1)
    end_date = datetime.date(2020, 12, 31)

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

    url = 'http://35.189.249.87/api/ride/show'

    hour = random.randint(10, 23)

    acc_d, acc_l = [], []
    try:
        for i in range(750):
            f_date, _ = generate_random_date_range()
            data = {
                's_Date' : str(f_date) + ' {}:00:00'.format(hour),
                'e_Date' : str(f_date) + ' {}:00:00'.format(hour+2)
            }
            t = datetime.datetime.today()
            res = reshome(url, data, 0)
            print('Requests made: {} | Execution time: {}'.format(i, res))
            acc_d.append(t)
            acc_l.append(res)
        return acc_d, acc_l
    except KeyboardInterrupt:
        return acc_d, acc_l

date, latency = simulate_increased_load()

now = datetime.datetime.now()

final = pd.DataFrame.from_dict(
{
    'Date': date,
    'Latency': latency
}
).to_csv('{}.csv'.format(now.strftime("%H:%M:%S")))

# df1 = pd.read_csv('default.csv', index_col=0)
# df4['rolling'] = df4.Latency.rolling(5).mean()

# sns.lineplot( x = 'Date',
#              y = 'Latency',
#              data = df4,
#              label = 'latency')
  
# sns.lineplot( x = 'Date',
#              y = 'rolling',
#              data = df4,
#              label = 'rolling')

# ax = plt.gca()
# ax.set_ylim([2, 5.5])
# ax.legend()
# plt.savefig('new.png')
