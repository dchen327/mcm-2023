import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import plotly.express as px

df = pd.read_csv('wordle.csv')

def scrabble_score(word):
    letter_points = {
        'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
        'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
        's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
    }
    return sum([letter_points.get(letter, 0) for letter in word.lower()])

# give a plot of Num_Rep_Results and Number_Hard_Mode over time
# reverse order of x axis
df = df.iloc[::-1]

# date to seconds from epoch
df['x'] = pd.to_datetime(df['Date']).astype(np.int64) // 10**9
df['y'] = df['Num_Rep_Results']

# get the x value at the peak y value
peak_x = df.iloc[df['y'].argmax()]['x']
df['x'] = df['x'][df['x'] > peak_x]
df['y'] = df['y'][df['x'] > peak_x]

# df drop na
df = df.dropna()

fig = px.line(df, x='x', y='y')
fig.show()

# Define the exponential decay function
def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

# Fit the exponential decay curve to the data
popt, pcov = curve_fit(exponential_decay, df['x'], df['y'])
print(popt)
ls = np.linspace(df['x'].min(), df['x'].max(), 1000)

# Create a scatter plot for the data
fig = px.scatter(df, x='x', y='y', title='Exponential Decay Fit')
fig.add_trace(px.line(x=ls, y=exponential_decay(ls, *popt)).data[0])
fig.show()
print('lol')
