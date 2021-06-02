import json
import pandas as pd
from langdetect import detect
import os
import argparse

parser = argparse.ArgumentParser(description='Preprocessing des données')
parser.add_argument('--frenchThreshold', type=float, default=0.8,
                    help='Lowest ratio of French to non-French text. Enter a value between 0 and 1.')
parser.add_argument('--decompressedSourceFilePath', type=str, default="./",
                    help='Path to the source file downloaded and decompressed by download.sh')
args = parser.parse_args()

print(os.system('head -1 {}'.format(args.decompressedSourceFilePath)))