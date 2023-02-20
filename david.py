#%%
import pandas as pd

df = pd.read_csv('wordle.csv')
df.head()
# %%
df['pct_hard_mode'] = df['hard_mode'] / df['total']