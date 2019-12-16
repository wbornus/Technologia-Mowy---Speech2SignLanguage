import Levenshtein
import pandas as pd
import numpy as np

df = pd.read_csv('phrases.csv')

phrases = pd.DataFrame(df).to_numpy()

phrases_clean = []
for row in phrases:
    tmp_row = []
    for column in row:
        if type(column) == str:
            tmp_row.append(column)
        # print(type(column))
    phrases_clean.append(tmp_row)

phrases_clean = np.array(phrases_clean)

distance1 = Levenshtein.distance(phrases_clean[0][0], phrases_clean[0][1])
print(phrases_clean[0][0])
print(phrases_clean[0][1])
print(distance1)

print('\n\n')

distance2 = Levenshtein.distance(phrases_clean[0][0], phrases_clean[1][0])
print(phrases_clean[0][0])
print(phrases_clean[1][0])
print(distance2)

print('\n\n')

str1 = 'mam problemy z gardłami'
str2 = 'boli mnie gardło'
distance3 = Levenshtein.distance(str1, str2)
print(str1)
print(str2)
print(distance3)
