import csv 
import json
import os 

def save_json(dict, filename):
    d = json.dumps(dict, indent=4)
    with open('./' + filename + '.json', 'w') as json_file:
        json_file.write(d)  

def remove_edge(UI_o, II_o ,IU_o, UII_train_quadruple_o, UII_valid_quadruple_o, UII_test_quadruple_o):
    UI = UI_o.copy()
    II = II_o.copy()
    IU = IU_o.copy()
    UII_train_quadruple = UII_train_quadruple_o.copy()
    UII_valid_quadruple = UII_valid_quadruple_o.copy()
    UII_test_quadruple = UII_test_quadruple_o.copy()

    for quadruples in UII_valid_quadruple + UII_test_quadruple:
        userid, given_item, positive_item, negative_item = quadruples
        if positive_item in UI[userid]:
            UI[userid].remove(positive_item)
        if positive_item in II[given_item]:
            II[given_item].remove(positive_item)
        if given_item in II[positive_item]:
            II[positive_item].remove(given_item)
        if userid in IU[positive_item]:
            IU[positive_item].remove(userid)

    for quadruples in UII_train_quadruple:
        userid, given_item, positive_item, negative_item = quadruples
        if positive_item in UI[userid]:
            UI[userid].remove(positive_item)
        if positive_item in II[given_item]:
            II[given_item].remove(positive_item)
        if given_item in II[positive_item]:
            II[positive_item].remove(given_item)
        if userid in IU[positive_item]:
            IU[positive_item].remove(userid)


    return UI,IU,II