import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# df = pd.read_csv('../data/farsi/clips/validated.csv')
df = pd.read_csv('../data/farsi/clips/other.csv')
arr = []
# print(df.columns.values)
# print(df['transcript'])

i = 0
for index, row in df.iterrows():
    # print( row["transcript"])

    # row["transcript"]=row["transcript"].replace('ـ', '')
    # row["transcript"]=row["transcript"].replace('،', '')
    # row["transcript"]=row["transcript"].replace('؟', '')
    # row["transcript"]=row["transcript"].replace('ك', 'ک')
    for char in row["transcript"]:
        i += 1
    # if char == 'ك':
    #     print(row)
    #     print(i)
        if char not in arr:
            arr.append(char)
# arr=arr.sort()
print(arr)
# print(len(arr))
with open('other_alphabet.txt', 'w') as alphaWrite:
    # Further file processing goes here
    for char in arr:
        alphaWrite.writelines(char+'\n')
    # print(alphaWrite.readlines())


# msk = np.random.rand(len(df)) < 0.8
# train = cdf[msk]