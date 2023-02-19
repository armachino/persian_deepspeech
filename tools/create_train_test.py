import pandas as pd
import sys
import os
import pathlib

import numpy as np
# from sklearn.model_selection import train_test_split

import argparse

parser = argparse.ArgumentParser(description="Description:  Input-> CSV Dataset.  |  OUTPUT-> Creates a test.csv & train.csv beside the Input dataset.")

parser.add_argument("--dataset_path", help="Path of the csv dataset.", )

args = parser.parse_args()



csv_file_path=os.path.abspath(args.dataset_path)
csv_dir_path=os.path.split(csv_file_path)[0]
# print("os.path.dirname(sys.argv[1])__>   ",os.path.abspath(sys.argv[1]))
# print("csv_dir_path  ",csv_dir_path)
# print("csv_dir_path  ",csv_dir_path)


df = pd.read_csv(csv_file_path)
# print(df.head())
msk = np.random.rand(len(df)) < 0.7
train = df[msk]
other = df[~msk]

validate_msk = np.random.rand(len(other)) < 0.5
test = other[validate_msk]
validate = other[~validate_msk]

print(train.shape)
print(test.shape)
print(validate.shape)

train_path=os.path.join(csv_dir_path,"train_.csv")
test_path=os.path.join(csv_dir_path,"test_.csv")
validate_path=os.path.join(csv_dir_path,"validate_.csv")
train.to_csv(train_path,index=False)
test.to_csv(test_path,index=False)
validate.to_csv(validate_path,index=False)
print(f"train_.csv creats at {train_path}")
print(f"test_.csv creats at {test_path}")
print(f"validate_.csv creats at {validate_path}")

