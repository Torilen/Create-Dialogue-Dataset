# -*- coding: utf-8 -*-

import json
import pandas as pd
from langdetect import detect_langs
import os
import argparse
import subprocess
import glob
import time
import math
import asyncio
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import torch
import re
import requests
from tqdm.notebook import tqdm

parser = argparse.ArgumentParser(description='Acquisition et traitement des données')
parser.add_argument('--languageThreshold', type=float, default=0.8,
                    help='Lowest ratio of language to non-language text. Enter a value between 0 and 1.')
parser.add_argument('--decompressedSourceFilePath', type=str, default="./data/",
                    help='Path to the source file downloaded and decompressed by download.sh')
parser.add_argument('--listSubredditFilePath', type=str, default="./acceptedSubreddit.txt",
                    help='Path to the file contains the list of accepted subreddit')
parser.add_argument('--maxCommentProcessed', type=int, default=20000,
                    help='Maximum number of comment processed')
parser.add_argument('--useSubredditFilter', type=bool, default=False,
                    help='Use subreddit file ?')
parser.add_argument('--downloadData', type=bool, default=False,
                    help='The data source are already downloaded ?')
parser.add_argument('--languageToExtract', type=str, default='',
                    help='The language you want to extract from reddit ["fr", "en", "es", etc]')
args = parser.parse_args()

class Stats:
    """Filtering stats"""

    def __init__(self):
        """Initialize an Utterance"""
        self.bots = 0
        self.total = 0
        self.removed = 0
        self.deleted = 0
        self.empties = 0
        self.non_language = 0
        self.low_language = 0
        self.bad_subreddit = 0
        self.ok = 0
        self.percent = 0


def extract_comments(decompressedSourceFilePath):
    stats = Stats()
    i = 1
    reach_end = False
    with open(args.listSubredditFilePath) as f:
        list_subreddit = f.readlines()
        list_subreddit = [e.replace("\n", "") for e in list_subreddit]
    f.close()

    print(list_subreddit)
    start = time.time()
    with open(decompressedSourceFilePath, 'r') as source_file:
        with open("./reddit_source_fr_preprocessed.csv", 'a') as file:
            for comment in source_file:
                i += 1
                if stats.ok < args.maxCommentProcessed:
                    stats.total += 1

                    if stats.total % 1000000 == 0:
                        print("=====================")
                        end = time.time()
                        stats.percent = stats.total / n_messages * 100
                        print(
                            "Processed: " + str(stats.total) + "\n STATS : " + json.dumps(stats.__dict__) + "TIME : " + str(
                                (end - start) / 60) + "min")
                        start = time.time()
                    if not comment == "\n":

                        if comment == "end\n":
                            reach_end = True
                        else:
                            comment_loaded = json.loads(comment)
                            body = comment_loaded["body"]

                            if args.useSubredditFilter:
                                is_bad_subreddit = comment_loaded["subreddit"] not in list_subreddit
                                if is_bad_subreddit: stats.bad_subreddit += 1; continue
                            is_a_bot = body.__contains__("I am a bot") or body.__contains__("I'm a bot")
                            if is_a_bot: stats.removed += 1; continue
                            is_deleted = body.__contains__("[deleted]")
                            if is_deleted: stats.deleted += 1; continue
                            is_removed = body.__contains__("[removed]")
                            if is_removed: stats.removed += 1; continue

                            is_empty = body.strip() == ""
                            if is_empty: stats.empties += 1; continue

                            if not args.languageToExtract == "":
                                try:
                                    languages = detect_langs(body[0:50])
                                except:
                                    stats.non_language += 1
                                    continue
                                not_language = languages[0].lang != args.languageToExtract
                                if not_language: stats.non_language += 1; continue

                                low_language = languages[0].prob < args.languageThreshold
                                if low_language: stats.low_language += 1; continue

                            # Le commentaire est valable
                            data = ';'.join([str(i), str(comment_loaded['author']),
                                             "\"" + comment_loaded['body'].replace("`", "'").replace("\"", "'") + "\"",
                                             str(comment_loaded['controversiality']),
                                             str(comment_loaded['created_utc']), str(comment_loaded['distinguished']),
                                             str(comment_loaded['id']),
                                             str(comment_loaded['parent_id']), str(comment_loaded['score']),
                                             "\"" + comment_loaded['subreddit'] + "\"",
                                             str(comment_loaded['subreddit_id'])])

                            file.write(data + "\n")

                            stats.ok += 1
                    else:
                        continue
                else:
                    break
            file.close()

def decompressFile(fileName):
    if "zst" in fileName:
        os.system("zstd -d {} --memory=2048M --threads=8".format(fileName))
    elif "bz2" in fileName:
        os.system("bzip2 -dk {}".format(fileName))
    else:
        os.system("xz -dk {}".format(fileName))


if __name__ == "__main__":
    n_messages = 208000000
    pd.DataFrame([], columns=["author", "body", "controversiality", "created_utc", "distinguished", "id", "parent_id",
                              "score", "subreddit", "subreddit_id"]).to_csv("./reddit_source_fr_preprocessed.csv",
                                                                            sep=";")

    listLinkDownload = requests.get("https://files.pushshift.io/reddit/comments/")
    listLinkDownload = list(set(["https://files.pushshift.io/reddit/comments/" + x.group() for x in
                                     re.finditer(r'RC_[0-9]{4}-[0-9]{2}.((bz2)|(zst)|(xz))', listLinkDownload.text)]))
    listFileName = [args.decompressedSourceFilePath+x.replace("https://files.pushshift.io/reddit/comments/", "") for x in listLinkDownload]
    listLinkDownload.sort()

    print(listFileName)

    for file in listFileName:
        if file in glob.glob(args.decompressedSourceFilePath+"*.*"):
            print("Start decompression of {}".format(file), flush=True)
            decompressFile(file)
        else:
            print("Downloading the file...")
            os.system("wget -P {} https://files.pushshift.io/reddit/comments/{}".format(args.decompressedSourceFilePath, file.split("/")[2]))

        extension = "xz"
        if "zst" in file:
            extension = "zst"
        elif "bz2" in file:
            extension = "bz2"

        decompressedSourceFilePath = file.replace("."+extension, "")
        print(decompressedSourceFilePath)
        start = time.time()
        extract_comments(decompressedSourceFilePath)
        print("Durée = {}s".format(time.time() - start))
        os.system("rm -rf {}".format(decompressedSourceFilePath))

