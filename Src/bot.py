import pandas as pd
import pickle
import sys

map_dir = "../Mappings/"
model_dir = "../ML/Models/"
type_map = ["batting", "bowling", "fielding"]

def file_to_dict(fl):
    lines = open(fl, 'r').readlines()
    dict = {}
    for line in lines:
        line = line.strip().lower()
        key, val = line.split('\t')
        dict[key] = val
    return dict

def get_val(input_text, search_type):
    map_file = map_dir+search_type+"_map.txt"
    dict = file_to_dict(map_file)
    for key in dict.keys():
        if not(input_text.find(key) == -1):
            return dict[key]
    return None

def predict_val(input_text, search_type):
    model_file = model_dir+search_type+"_model.sav"
    vec_file = model_dir+search_type+".vec"

    clf = pickle.load(open(model_file,'rb'))
    vectorizer = pickle.load(open(vec_file,'rb'))
    
    pred = clf.predict(vectorizer.transform([input_text]))
    return pred[0]

def fill_template(input_text):
    input_text = input_text.lower()
    class_val = predict_val(input_text, "format")
    home_or_away = None#get_val(input_text, "")
    team = get_val(input_text, "team")
    type_val = type_map[predict_val(input_text, "type")]
    
    template = ""
    template += "class="+str(class_val)+";"
    if not(home_or_away == None):
        template += "home_or_away="+str(home_or_away)+";"
    if not(team == None):
        template += "team="+str(team)+";"
    if not(type_val == None):
        template += "type="+str(type_val)+";"

    template += "template=results"
    return template

base_url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?"
while True:

    line = sys.stdin.readline()
    if not line:
        break
    search_term = fill_template(line)

    final_query = base_url+search_term
    print(final_query)

    #tables = pd.read_html(final_query)
    #table = tables[2]
    #print(table)

#result = table[['Player', 'Ave']][table['Mat']>=10]
#print(result[:4])
