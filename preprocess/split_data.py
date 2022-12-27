import csv 
import json
import os 
import random

def compute_all_uii():
    iqon_pair_path = os.path.join('./iqon_data_pair.json')
    iqon_pair = json.load(open(iqon_pair_path, 'r'))

    item_metadata_path = os.path.join('./iqon_item_metadata_all.json')
    item_metadata = json.load(open(item_metadata_path, 'r'))

    def save_json(dict, filename):
        d = json.dumps(dict, indent=4)
        with open('./' + filename + '.json', 'w') as json_file:
            json_file.write(d)  

    UII = []

    for userid in list(iqon_pair.keys()):
        
        outfit = iqon_pair[userid]
        for o in outfit:
            outfit_id = list(o.keys())[0]
            item1_id = o[outfit_id][0]
            item2_id = o[outfit_id][1]

            uii = [userid, item1_id, item2_id]
            uii2 = [userid, item2_id, item1_id]
            if uii not in UII and uii2 not in UII:
                UII.append(uii)

    # save_json(UII, 'UII')
    return UII

def split_train_valid_test(UII_o):
    UII = UII_o.copy()
    random.shuffle(UII)

    UII_train_keep = UII[0: int(0.6 * len(UII))]
    UII_train_loss = UII[int(0.6 * len(UII)): int(0.8 * len(UII))]
    UII_valid = UII[int(0.8 * len(UII)): int(0.9 * len(UII))]
    UII_test = UII[int(0.9 * len(UII)):]
    return UII_train_keep, UII_train_loss, UII_valid, UII_test

def sample_negative(triplet_json_o):
    triplet_json = triplet_json_o.copy()

    iqon_pair_path = os.path.join('./iqon_data_pair.json')
    iqon_pair = json.load(open(iqon_pair_path, 'r'))
    tops = []
    bottoms = []
    for userid in list(iqon_pair.keys()):
    
        outfit = iqon_pair[userid]
        for o in outfit:
            outfit_id = list(o.keys())[0]
            top = o[outfit_id][0]
            bottom = o[outfit_id][1]
            if top not in tops:
                tops.append(top)
            if bottom not in bottoms:
                bottoms.append(bottom)

    def compute_quadruple(json_file):
        quadruple = []
        for triplet in json_file:
            userid = triplet[0]
            given_item_id = random.randint(1,2)
            given_item = triplet[given_item_id]
            top_bottom = triplet[1:]
            top_bottom.remove(given_item)
            positive_item = top_bottom[0]

            negative_item = positive_item
            if given_item_id == 1:
                while negative_item == positive_item:
                    negative_item = random.choice(bottoms)
            else:
                while negative_item == positive_item:
                    negative_item = random.choice(tops)
            quadruple.append([userid, given_item, positive_item, negative_item])
        return quadruple
    return compute_quadruple(triplet_json)

     


