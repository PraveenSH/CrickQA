import pandas as pd

map_dir = "./Mappings/"

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

def fill_template(input_text):
    input_text = input_text.lower()
    class_val = get_val(input_text, "format")
    home_or_away = 2#get_val(input_text, "")
    team = get_val(input_text, "team")
    type_val = get_val(input_text, "type")
    
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
search_term = fill_template("highest runs in ODI")

final_query = base_url+search_term
print(final_query)
tables = pd.read_html(final_query)
table = tables[2]
#print(table)

#result = table[['Player', 'Ave']][table['Mat']>=10]
#print(result[:4])
