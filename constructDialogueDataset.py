import pandas as pd
import json
import time
import argparse
k = dict()
p = set()

parser = argparse.ArgumentParser(description='Construction des données dialogues')
parser.add_argument('--extractedPreprocessCsvFilePath', type=str, default="./reddit_source_fr_preprocessed.csv",
                    help='Path to the source file preprocessed by getAndConcatData.py')
args = parser.parse_args()

def getAllParents(id, data):
    parent = data[data['id'] == id]['parent_id'].values
    if not len(parent) == 0:
        if type(parent[0]) == str:
            p.add(parent[0][3:])
            return getAllParents(parent[0][3:], data) + [parent[0][3:]]
        else:
            return [id]
    else:
        return [id]

def flat_tree_to_conv(tree, cur=()):
    root = list(tree.keys())[0]
    if tree[root] is None:
        yield cur+(root,)
    else:
        for childtree in tree[root]:
            for path in flat_tree_to_conv(childtree, cur+(root,)):
                yield path

def get_structure_conv(root):
    if root in dict_parent_children:
        childs = dict_parent_children[root]
        if len(childs) == 1:
            child = childs[0]
            if not child in dict_id_message:
                #print("STOP")
                return root
            else:
                #print("ONE CHILD "+child)
                return [{child: get_structure_conv(child)}]
        else:
            #print("MANY CHILD")
            return [{child: get_structure_conv(child)} for child in childs]

if __name__ == "__main__":
    data = pd.read_csv(args.extractedPreprocessCsvFilePath, sep=";", error_bad_lines=False)
    ld = len(data)
    dict_id_message = dict()
    dict_parent_children = dict()
    print("STEP 1/5")
    start = time.time()
    for i, row in data.iterrows():
        dict_id_message[row['id']] = (
        row['author'], row['body'], row['controversiality'], row['score'], row['subreddit'], row['parent_id'])
        if row['parent_id'][3:] in dict_parent_children:
            dict_parent_children[row['parent_id'][3:]].append(row['id'])
        else:
            dict_parent_children[row['parent_id'][3:]] = [row['id']]
        if i % 100000 == 0:
            end = time.time()
            time_for_1_epoch = end - start
            time_for_1_epoch_min = time_for_1_epoch / 60
            print("{}/{} Temps restant : {} min - Delay : {}s".format(i, ld, (ld - i) / 100000 * time_for_1_epoch_min,
                                                                      time_for_1_epoch))
            start = time.time()

    ldpc = len(dict_parent_children)
    print("STEP 2/5")
    root_list = list()
    i = 0
    start = time.time()
    for ke in dict_parent_children:
        i += 1
        if not ke in dict_id_message:
            root_list += dict_parent_children[ke]

        if i % 100000 == 0:
            end = time.time()
            time_for_1_epoch = end - start
            time_for_1_epoch_min = time_for_1_epoch / 60
            print(
                "{}/{} Temps restant : {} min - Delay : {}s".format(i, ldpc, (ldpc - i) / 100000 * time_for_1_epoch_min,
                                                                    time_for_1_epoch))
            start = time.time()
    print(len(root_list))
    print("STEP 3/5")
    lrl = len(root_list)
    res2 = []
    i = 0
    start = time.time()
    for root in root_list:
        res = get_structure_conv(root)
        if res is not None:
            res2.append({root: res})
        i += 1
        if i % 100000 == 0:
            end = time.time()
            time_for_1_epoch = end - start
            time_for_1_epoch_min = time_for_1_epoch / 60
            print("{}/{} Temps restant : {} min - Delay : {}s".format(i, lrl, (lrl - i) / 100000 * time_for_1_epoch_min,
                                                                      time_for_1_epoch))
            start = time.time()

    i = 0
    start = time.time()
    convs = []
    stats = dict()
    print("STEP 4/5")
    for r in res2:
        conv = list(flat_tree_to_conv(r))
        for discussion in conv:
            convs.append(discussion)
            len_discussion = len(conv)
            if len_discussion in stats:
                stats[len_discussion] += 1
            else:
                stats[len_discussion] = 1
        i += 1
        if i % 100000 == 0:
            end = time.time()
            time_for_1_epoch = end - start
            time_for_1_epoch_min = time_for_1_epoch / 60
            print("{}/{} Temps restant : {} min - Delay : {}s".format(i, len(res2),
                                                                      (len(res2) - i) / 100000 * time_for_1_epoch_min,
                                                                      time_for_1_epoch))
            start = time.time()

    convs_json = {}
    id_conv = 0
    print("STEP 5/5")
    start = time.time()
    for conv in convs:
        c = {}
        for message_id in conv:
            data_message = dict_id_message[message_id]
            c[message_id] = {"author": data_message[0], "message": data_message[1], "controversiality": data_message[2],
                             "score": data_message[3], "subreddit": data_message[4]}
        convs_json[id_conv] = c
        id_conv += 1

        if id_conv % 100000 == 0:
            end = time.time()
            time_for_1_epoch = end - start
            time_for_1_epoch_min = time_for_1_epoch / 60
            print("{}/{} Temps restant : {} min - Delay : {}s".format(id_conv, len(convs), (
                        len(convs) - id_conv) / 100000 * time_for_1_epoch_min, time_for_1_epoch))
            start = time.time()
    with open("./fr_reddit_dataset.json", "w") as outfile:
        json.dump(convs_json, outfile)