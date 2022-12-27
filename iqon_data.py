import csv 
import json
import os 
import random

item_img_num = open('./item_img_num.csv', encoding='utf-8')
item_img_num = csv.reader(item_img_num)

item_meta_data_path = os.path.join('./', 'iqon_item_metadata_all.json')
item_meta_data = json.load(open(item_meta_data_path, 'r'))

IQON_root_path = '**' # IQON3000 datapath
user_ids = os.listdir(IQON_root_path)

def select_up_bottom(items):
    top_semantic = ['8', '9']
    bottom_semantic = ['1', '7', '16']

    top_category = ['11','12', '18', '19', '33', '37', '46']
    bottom_category = ['1','10', '25', '40', '52']
    tops = []
    bottoms = []
    for i in items:
        semantic_category_i = item_meta_data[i]['semantic_category']
        category_i = item_meta_data[i]['category_id']
        if semantic_category_i in top_semantic and category_i in top_category:
            tops.append(i)
        elif semantic_category_i in bottom_semantic and category_i in bottom_category:
            bottoms.append(i)
    if len(tops) > 0 and len(bottoms) > 0:
        top = random.choice(tops)
        bottom = random.choice(bottoms)
        return [top, bottom]
    else:
        return []

IQON_top_bottom = {}
top_bottom_outfit_dict = {}

for user in user_ids:
    outfit_ids = os.listdir(os.path.join(IQON_root_path,user))
    for outfit in outfit_ids:
        item_file_path = os.path.join(IQON_root_path, user, outfit)
        for item_ids in os.listdir(item_file_path):
            if item_ids[-4:] == 'json':
                try:
                    data = json.load(open(os.path.join(IQON_root_path, user, outfit, item_ids), 'r'))
                except:
                    print(os.path.join(IQON_root_path, user, outfit, item_ids))
                    ##### continue
                    
                outfit_id = str(data['setId'])
                user_id = str(data['user'])
                item_id = []
                for i in data['items']:
                    item_id.append(str(i['itemId']))
                #print(item_id)
                top_bottom = select_up_bottom(item_id)
                if len(top_bottom) == 2:
                    temp_list = [user_id, outfit_id] + top_bottom
                    if top_bottom[0] + '_' + top_bottom[1] not in top_bottom_outfit_dict:
                        top_bottom_outfit_dict[top_bottom[0] + '_' + top_bottom[1]] = outfit_id
                    else:
                        outfit_id = top_bottom_outfit_dict[top_bottom[0] + '_' + top_bottom[1]]    #### 共用一个outfit_id，可能导致找不到对应路径
                    if user_id not in IQON_top_bottom:
                        IQON_top_bottom[user_id] = []
                    else:
                        if outfit_id not in IQON_top_bottom[user_id]:
                            IQON_top_bottom[user_id].append({outfit_id:top_bottom})
                else:
                    pass


json_iqon_top_bottom = json.dumps(IQON_top_bottom, indent=4)
with open('./iqon_data_pair.json', 'w') as json_file:
    json_file.write(json_iqon_top_bottom)

# top_bottom_outfit_dict = json.dumps(top_bottom_outfit_dict, indent=4)
# with open('./top_bottom_outfit2.json', 'w') as json_file:
#     json_file.write(top_bottom_outfit_dict)
