import pandas as pd
import json
import argparse

k = dict()
p = set()

parser = argparse.ArgumentParser(description='Construction des données dialogues')
parser.add_argument('--extractedPreprocessCsvFilePath', type=str, default="./",
                    help='Path to the source file preprocessed by preprocess.py')
args = parser.parse_args()

def getAllParents(id, data):
    parent = data[data['id'] == id]['parent_id'].values
    if not len(parent) == 0:
        p.add(parent[0][3:])
        return getAllParents(parent[0][3:], data) + [parent[0][3:]]
    else:
        return [id]

if __name__ == "__main__":
    data = pd.read_csv(args.extractedPreprocessCsvFilePath, sep=";", error_bad_lines=False)
    print(data.describe())
    print(data.head())
    j = 0
    for i, row in data.iterrows():
        if not row['id'] in p:
            parents = getAllParents(row['id'], data)[1:]
            last_element = parents[len(parents)-1]
            if last_element in list(k.keys()):
                del k[last_element]
                k[row['id']] = parents+[row['id']]
            else:
                k[row['id']] = parents + [row['id']]

        if j % 10000 == 0:
            print("{}/{}".format(j, len(data)))
        #if row['id'] in list(k.keys()):
    print(len(k))
    #print(getAllParents(row['id'], data)[1:])