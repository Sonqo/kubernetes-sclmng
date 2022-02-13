import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# df = pd.concat([
#     pd.read_csv('a.csv'),
#     pd.read_csv('b.csv'),
#     pd.read_csv('c.csv'),
# ])

df = pd.read_csv('output.csv')

df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')
df.to_csv('new.csv')
# df['timeStamp'] = df['timeStamp'].dt.time
df = df[['timeStamp', 'Latency']]

df['rolling'] = df['Latency'].rolling(10).mean()

# df = df.reset_index()

sns.set(rc={'figure.figsize':(16,8)})

sns.lineplot(
    x = df['timeStamp'],
    y = df['Latency'],
    data = df,
    label = 'latency'
)

sns.lineplot(
    x = df['timeStamp'],
    y = df['rolling'],
    data = df,
    label = 'rolling'
)

plt.savefig('foo.png')