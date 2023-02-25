import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

import argparse

parser = argparse.ArgumentParser(description="Description:  Input-> CSV Dataset.  |  OUTPUT-> Replace or delete desierd Character or ignore the file .")

parser.add_argument("--dataset_path", help="Path of the csv dataset.", )

args = parser.parse_args()

csv_file_path=os.path.abspath(args.dataset_path)
csv_dir_path=os.path.split(csv_file_path)[0]
csv_file_name=os.path.split(csv_file_path)[1]

print('os.path.split(csv_file_path)[0]',os.path.split(csv_file_path)[0])
print('os.path.split(csv_file_path)[1]',os.path.split(csv_file_path)[1])
df = pd.read_csv(csv_file_path)
# alpha=["آ","ا",'',"ً","ِ","ٔ","ب","پ","ت","ث","ج","چ","ح","خ","د","ذ","ر","ز","ژ","س","ش","ص","ض","ط","ظ","ع","غ","ف","ق","ک","گ","ل","م","ن","و","ه","ی","ئ"," "]


with open('alphabets.txt') as f:
    alpha = [line.rstrip() for line in f]
    alpha=alpha[:-1]
    alpha[0]=' '

print(alpha)

print(df.columns.values)

## Remove or replace characters here.
df['transcript'] = df['transcript'].str.replace('ـ', '')
df['transcript'] = df['transcript'].str.replace('،', '')
df['transcript'] = df['transcript'].str.replace('؟', '')
df['transcript'] = df['transcript'].str.replace('ك', 'ک')

ext_chars = [] # External characters.
for index, row in df.iterrows():

    for char in row["transcript"]:
        if char not in alpha:
            ext_chars.append(char)
            print(f"asci code : {ord(char)} , chara: {char}")
            print(row["transcript"],'\n****')

# arr = list(dict.fromkeys(arr))
print(ext_chars)
is_alpha_match=True
for index, row in df.iterrows():
    for char in row["transcript"]:
        if char not in alpha:
            is_alpha_match=False
            print(f"Characet {char} is not exist in this transcribe.")
            print(f"wav_filename {row['wav_filename']} transcript: {row['transcript']}. \n")

if is_alpha_match:
    print("\n** All dataset transcribe is included with the alphabet file. ")
    dataset_path=os.path.join(csv_dir_path,"fixed_"+csv_file_name)
    df.to_csv(dataset_path,index=False)
    print(f"** {'fixed_'+csv_file_name} creats at {csv_dir_path}")
else:
    print("\n ** Dataset is used external alphabet character. check the dataset and alphabet to create fixed_words.csv file. \n")
    
