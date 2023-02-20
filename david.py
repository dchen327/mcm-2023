#%%
import pandas as pd
import plotly.express as px

df = pd.read_csv('wordle.csv')
df.head()
print(df.columns)
# %%
df['Pct_Hard_Mode'] = df['Number_Hard_Mode'] / df['Num_Rep_Results']
df.head()

# visualize all column distributions
for col in df.columns:
    fig = px.histogram(df, x=col, nbins=100)
    fig.show()