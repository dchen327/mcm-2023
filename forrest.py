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
fig = px.line(df, x='Date', y=['Num_Rep_Results', 'Number_Hard_Mode'])
fig.show()
