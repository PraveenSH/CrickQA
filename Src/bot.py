import pandas as pd
import pickle
import sys

map_dir = "../Mappings/"
model_dir = "../ML/Models/"

type_map = ["batting", "bowling", "fielding", "fow"]
batting_map = ["runs","batting_average","high_score", "fifty_plus", "hundreds", "ducks", "notouts"]
bowling_map = ["concede", "wickets", "bbi", "economy_rate", "four_plus_wickets", "five_wickets", "bowling_average"]
fielding_map = ["dismissals", "caught", "stumped", "caught_keeper", "caught_fielder"]

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
    class_val = predict_val(input_text, "format")+1
    home_or_away = None#get_val(input_text, "")
    team = get_val(input_text, "team")
    type_val = type_map[predict_val(input_text, "type")]

    if type_val == "batting":
        orderby_val = batting_map[predict_val(input_text, "batting")]
    if type_val == "bowling":
        orderby_val = bowling_map[predict_val(input_text, "bowling")]
    if type_val == "fow":
        orderby_val = "fow_"+batting_map[predict_val(input_text, "batting")]
    if type_val == "fielding":
        orderby_val = fielding_map[predict_val(input_text, "fielding")]


    template = ""
    template += "class="+str(class_val)+";"
    if not(home_or_away == None):
        template += "home_or_away="+str(home_or_away)+";"
    if not(team == None):
        template += "team="+str(team)+";"
    if not(type_val == None):
        template += "type="+str(type_val)+";"
    if not(orderby_val == None):
        template += "orderby="+str(orderby_val)+";"

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

    tables = pd.read_html(final_query)
    table = tables[2]
    player = table['Player'][0]
    print(player)
