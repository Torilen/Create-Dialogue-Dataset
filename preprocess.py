# -*- coding: utf-8 -*-

import json
import pandas as pd
from langdetect import detect_langs
import os
import argparse
import subprocess
import time

parser = argparse.ArgumentParser(description='Preprocessing des données')
parser.add_argument('--frenchThreshold', type=float, default=0.8,
                    help='Lowest ratio of French to non-French text. Enter a value between 0 and 1.')
parser.add_argument('--decompressedSourceFilePath', type=str, default="./",
                    help='Path to the source file downloaded and decompressed by download.sh')
parser.add_argument('--listSubredditFilePath', type=str, default="./",
                    help='Path to the file contains the list of accepted subreddit')
parser.add_argument('--maxCommentProcessed', type=int, default=20000,
                    help='Maximum number of comment processed')
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
        self.non_french = 0
        self.low_french = 0
        self.bad_subreddit = 0
        self.ok = 0

if __name__ == "__main__":
    stats = Stats()
    reach_end = False
    i = 1
    pd.DataFrame([], columns=["author", "body", "controversiality", "created_utc", "distinguished", "id", "parent_id",
                              "score", "subreddit", "subreddit_id"]).to_csv("./reddit_source_fr_preprocessed.csv", sep=";")
    with open(args.listSubredditFilePath) as f:
        list_subreddit = f.readlines()
        list_subreddit = [e.replace("\n", "") for e in list_subreddit]
    f.close()

    print(list_subreddit)
    start = time.time()
    with open(args.decompressedSourceFilePath, 'r') as source_file:
        for comment in source_file:
            if stats.ok < args.maxCommentProcessed:
                i += 1
                stats.total += 1
                if not comment == "\n":
                    if comment == "end\n":
                        reach_end = True
                    else:
                        comment_loaded = json.loads(comment)
                        body = comment_loaded["body"]

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

                        try:
                            languages = detect_langs(body[0:50])
                        except:
                            stats.non_french += 1
                            continue

                        not_french = languages[0].lang != 'fr'
                        if not_french: stats.non_french += 1; continue

                        low_french = languages[0].prob < args.frenchThreshold
                        if low_french: stats.low_french += 1; continue

                        # Le commentaire est valable
                        comment_id = comment_loaded['id']
                        data = ';'.join([str(i), str(comment_loaded['author']), "\""+comment_loaded['body'].replace("`", "'").replace("\"", "'")+"\"", str(comment_loaded['controversiality']),
                                         str(comment_loaded['created_utc']), str(comment_loaded['distinguished']), str(comment_loaded['id']),
                                         str(comment_loaded['parent_id']), str(comment_loaded['score']), "\""+comment_loaded['subreddit']+"\"",
                                         str(comment_loaded['subreddit_id'])])
                        #subprocess.check_output("echo `{}` >> ./reddit_source_fr_preprocessed.csv".format(data), shell=True)
                        with open("./reddit_source_fr_preprocessed.csv", 'a') as file:
                            file.write(data+"\n")
                        file.close()
                        stats.ok += 1
                        print("=====================")
                        print(stats.total)
                        if stats.total % 10000 == 0:
                            print("=====================")
                            end = time.time()
                            print("Processed: " + str(stats.total) + "\n STATS : " + json.dumps(stats.__dict__) + "TIME : " + str((end-start)/60) + "min")
                            start = time.time()
                else:
                    stats.empties += 1
                    continue
            else:
                break



