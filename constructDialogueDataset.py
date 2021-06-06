import pandas as pd
import json
import argparse

k = dict()
p = list()

parser = argparse.ArgumentParser(description='Construction des données dialogues')
parser.add_argument('--extractedPreprocessCsvFilePath', type=str, default="./",
                    help='Path to the source file preprocessed by preprocess.py')
args = parser.parse_args()

if __name__ == "__main__":
    data = pd.read_csv(args.extractedPreprocessCsvFilePath, sep=";")
    print(data.describe())
    print(data.head())