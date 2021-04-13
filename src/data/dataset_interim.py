# Importing Libraries and Packages
import os

import json
import glob

import argparse

import pandas as pd


# Creating Directory for Subject
def create_dir(id):
    if not os.path.exists(f'data/interim/{id}'):
        os.makedirs(f'data/interim/{id}')

# Creating Dataframes for the JSON files
def create_dataframes(directory):
    create_dir(directory.rsplit("/")[-2])
    files = glob.glob(f"{directory}*.json")
    for file in files:
        try:
            data = json.load(open(file))
            df1 = pd.DataFrame(data['IRLED']).T
            df1.columns = ['IRLED']
            df1['index'] = pd.DataFrame(range(len(df1)))

            df2 = pd.DataFrame(data['REDLED']).T
            df2.columns = ['REDLED']
            df2['index'] = pd.DataFrame(range(len(df2)))

            merged_df = df1.merge(df2, on = 'index')
            merged_df.drop('index', axis = 1, inplace = True)
            merged_df = merged_df.apply(pd.to_numeric)
            merged_df.to_csv('data/interim/' + f'{file.rsplit("/", 2)[-2]}' + "/" + f'{file.rsplit("/", 1)[-1][:-5]}' + '.csv')
            print(f'{file} is processed!')
        except:
            print('\n')
            print(f'{file} has some issues!')
            print('\n')
    print("All Files Processed!")


if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()

    # currently, we only need filepath to the image
    parser.add_argument("--dir", type=str)

    # read the arguments from the command line
    args = parser.parse_args()

    # run the predict specified by command line arguments
    create_dataframes(directory=args.dir)