#%%
import pandas as pd
import plotly.express as px

df = pd.read_csv('wordle.csv')
df.head()
print(df.columns)
# %%
df['Pct_Hard_Mode'] = df['Number_Hard_Mode'] / df['Num_Rep_Results']
df['Date'] = pd.to_datetime(df['Date'])
df.head()

# visualize Num_Rep_Results over time
fig = px.line(df, x='Date', y='Num_Rep_Results', title='Number of Rep Results')
fig.show()