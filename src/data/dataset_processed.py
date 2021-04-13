# Importing Libraries and Packages
import os
import glob

import neurokit2 as nk

import pandas as pd

import argparse


# Creating Directory for Subject
def create_dir(id):
    if not os.path.exists(f'data/processed/{id}'):
        os.makedirs(f'data/processed/{id}')


def create_signals(directory):
    create_dir(directory.rsplit("/")[-2])
    files = glob.glob(f"{directory}*.csv")
    for sample in files:
        try:
            dataframe = pd.read_csv(sample)
            signals, info = nk.ppg_process(dataframe['IRLED'][10:-1], sampling_rate=100)
            signals.to_csv('data/processed/' + f'{sample.rsplit("/", 2)[-2]}' + "/" + f'{sample.rsplit("/", 1)[-1][:-4]}' + '.csv')
            print(f"{sample} is processed!")
        except:
            print(f"{sample} has some issues!")


if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()

    # currently, we only need filepath to the image
    parser.add_argument("--dir", type=str)

    # read the arguments from the command line
    args = parser.parse_args()

    # run the predict specified by command line arguments
    create_signals(directory=args.dir)