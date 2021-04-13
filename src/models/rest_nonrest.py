# Importing Libraries & Packages
import glob
import argparse

from collections import Counter

import pandas as pd


def predict(directory):
    signals = glob.glob(f"{directory}*.csv")
    for file in signals:
        try:
            dataframe = pd.read_csv(file)
            label_dict = Counter(dataframe["PPG_Peaks"])
            if label_dict[1.0] > 1:
                print(f'{file.rsplit("/", 1)[-1][:-4]}' + ' is a non-resting sample!')
                print('\n')
            else:
                print(f'{file.rsplit("/", 1)[-1][:-4]}' + ' is a resting sample!')
                print('\n')
        except:
            print(f'{file.rsplit("/", 1)[-1][:-4]}' + ' has some issues!')



if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()

    # currently, we only need filepath to the image
    parser.add_argument("--dir", type=str)

    # read the arguments from the command line
    args = parser.parse_args()

    # run the predict specified by command line arguments
    predict(directory=args.dir)