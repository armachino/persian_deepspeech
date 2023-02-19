import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


df = pd.read_csv('../data/farsi_/clips/validated.csv')
alpha=["آ","ا","ً","ِ","ٔ","ب","پ","ت","ث","ج","چ","ح","خ","د","ذ","ر","ز","ژ","س","ش","ص","ض","ط","ظ","ع","غ","ف","ق","ک","گ","ل","م","ن","و","ه","ی","ئ"," "]

print(df.columns.values)

arr = []
i=0
for index, row in df.iterrows():
    # print( row["transcript"])

    # row["transcript"]=row["transcript"].replace('ـ', '')
    # row["transcript"]=row["transcript"].replace('،', '')
    # row["transcript"]=row["transcript"].replace('؟', '')
    # row["transcript"]=row["transcript"].replace('ك', 'ک')
    for char in row["transcript"]:
        i += 1
        if char not in alpha:
            print(char)
            print(row["transcript"])
            print("****")
    # if char == 'ك':
    #     print(row)
    #     print(i)
        # if char not in arr:
        #     arr.append(char)
# arr=arr.sort()
print(arr)

# for index, row in df.iterrows():
#     # print( row["transcript"])

#     row["transcript"]=row["transcript"].replace('ـ', '')
#     row["transcript"]=row["transcript"].replace('،', '')
#     row["transcript"]=row["transcript"].replace('؟', '')
#     row["transcript"]=row["transcript"].replace('ك', 'ک')
#     for char in row["transcript"]:
#         i += 1

#         if char not in arr:
#             arr.append(char)
