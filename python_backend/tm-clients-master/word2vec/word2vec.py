from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import math
df = pd.read_csv('phrases.csv')

phrases = pd.DataFrame(df).to_numpy()

phrases_clean = []
for row in phrases:
    tmp_row = []
    for column in row:
        if type(column) == str:
            tmp_row.append(column)
        print(type(column))
    phrases_clean.append(tmp_row)

phrases_clean = np.array(phrases_clean)

print(phrases_clean)

model = Word2Vec(phrases_clean, min_count=1, size=5, workers=3, window=1, sg=0)

print(model['kardiolog'])

print(model.similarity('głowa', 'mam ból głowy'))
print(model.similarity('głowa', 'witam'))

print(model.most_similar('witam')[:5])