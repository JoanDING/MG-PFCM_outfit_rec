import csv 
import json
import os 


def compute_origin_edge():
    iqon_pair_path = os.path.join('./iqon_data_pair.json')
    iqon_pair = json.load(open(iqon_pair_path, 'r'))

    item_metadata_path = os.path.join('./iqon_item_metadata_all.json')
    item_metadata = json.load(open(item_metadata_path, 'r'))

    UI = {}
    IU = {}

    II = {}
    all_item = []

    IA = {}
    AI = {}

    for userid in list(iqon_pair.keys()):
        if userid not in UI:
            UI[userid] = []
        
        outfit = iqon_pair[userid]
        for o in outfit:
            outfit_id = list(o.keys())[0]
            item1_id = o[outfit_id][0]
            item2_id = o[outfit_id][1]
            if item1_id not in all_item:
                all_item.append(item1_id)
            if item2_id not in all_item:
                all_item.append(item2_id)
            
            ## UI ##
            if item1_id not in UI[userid]:
                UI[userid].append(item1_id)
            if item2_id not in UI[userid]:
                UI[userid].append(item2_id)
            
            ## IU ##
            if item1_id not in IU:
                IU[item1_id] = []
            if userid not in IU[item1_id]:
                IU[item1_id].append(userid)
            if item2_id not in IU:
                IU[item2_id] = []
            if userid not in IU[item2_id]:
                IU[item2_id].append(userid)
            
            ## II ##
            if item1_id not in II:
                II[item1_id] = []
            if item2_id not in II[item1_id]:
                II[item1_id].append(item2_id)
            if item2_id not in II:
                II[item2_id] = []
            if item1_id not in II[item2_id]:
                II[item2_id].append(item1_id)
            
    def save_json(dict, filename):
        d = json.dumps(dict, indent=4)
        with open('./dict/' + filename + '.json', 'w') as json_file:
            json_file.write(d)        

    # save_json(UI, 'UI')
    # save_json(IU, 'IU')
    # save_json(II, 'II')

    for item_id in all_item:
        IA[item_id] = []
        item_attribute = item_metadata[item_id]['title']
        for index, attribute in enumerate(item_attribute):
            if index == 2:
                continue
            if attribute != 0:
                attribute_id = str(index) + '_' + str(attribute) 
                IA[item_id].append(attribute_id)

                if attribute_id not in AI:
                    AI[attribute_id] = []
                if item_id not in AI[attribute_id]:
                    AI[attribute_id].append(item_id)

    # save_json(IA, 'IA')
    # save_json(AI, 'AI')
    return UI,IU,II,IA,AI
