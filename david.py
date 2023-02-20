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
# %%
# Feature generation
# uncommon letters are ZQJXKVBYWGP
def has_uncommon_letters(word):
    uncommon_letters = set('zqjxkvbywgp')
    return any(letter in uncommon_letters for letter in word)

df['Has_Uncommon_Letters'] = df['Word'].apply(has_uncommon_letters)



# %%
# feature for how close a given word is to all other possible wordle words
with open('wordle_words.txt') as f:
    wordle_words = set(f.read().splitlines())

def distance_to_wordle_words(word):
    return sum(levenshtein(word, wordle_word) <= 2 for wordle_word in wordle_words)

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

df['Distance_To_Wordle_Words'] = df['Word'].apply(distance_to_wordle_words)

def scrabble_score(word):
    letter_points = {
        'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
        'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
        's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
    }
    return sum([letter_points.get(letter, 0) for letter in word.lower()])

df['Scrabble_Score'] = df['Word'].apply(scrabble_score)
df['Scrabble_Score'].describe()