import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# df = pd.read_csv('../data/farsi/clips/validated.csv')
df = pd.read_csv('../data/farsi/clips/other.csv')
arr = []

for index, row in df.iterrows():
    for char in row["transcript"]:
        if char not in arr:
            arr.append(char)

print(arr)

with open('other_alphabet.txt', 'w') as alphaWrite:
    # Further file processing goes here
    for char in arr:
        alphaWrite.writelines(char+'\n')