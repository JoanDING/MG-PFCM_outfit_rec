
from compute_origin_edge import *
from split_data import *
from remove_edge import *
import os 

def save_json(dict, type, filename):
    d = json.dumps(dict, indent=4)
    with open(os.path.join('./preprocess', type, filename + '.json'), 'w') as json_file:
        json_file.write(d)  

if __name__ == '__main__':
    # compute adjacency list
    UI,IU,II,IA,AI = compute_origin_edge()
    # split train-valid-test
    UII = compute_all_uii()
    UII_train_keep, UII_train_loss, UII_valid, UII_test = split_train_valid_test(UII)

    # sample negative item to construst quadruple data
    UII_train_quadruple_keep = sample_negative(UII_train_keep)
    UII_train_quadruple = sample_negative(UII_train_loss)
    UII_valid_quadruple = sample_negative(UII_valid)
    UII_test_quadruple = sample_negative(UII_test)

    # remove edge of the training/validation/testing data from UI/IU/II
    UI,IU,II = remove_edge(UI,II,IU,UII_train_quadruple,UII_valid_quadruple,UII_test_quadruple)

    # save data for graph method
    for d in zip([UI, IU, II, IA, AI], ['UI', 'IU', 'II', 'IA', 'AI']):
        save_json(d[0], 'graph_data', d[1])
    for d in zip([UII_train_quadruple, UII_valid_quadruple, UII_test_quadruple], ['UII_train_quadruple', 'UII_valid_quadruple', 'UII_test_quadruple']):
        save_json(d[0], 'graph_data', d[1])

    # save data for non-graph method
    for d in zip([UII_train_quadruple + UII_train_quadruple_keep, UII_valid_quadruple, UII_test_quadruple], ['UII_train_quadruple', 'UII_valid_quadruple', 'UII_test_quadruple']):
        save_json(d[0], 'non-graph_data', d[1])