import os
import sys
import collections
import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup
import lxml.html as lh
import requests

team_ids = 10
match_type = ["test","odi","t20"]
match_type_ids = 3
pages = 5
player_type = ["batting","bowling","fielding","partnership","team"]
venue = 3
base_url = "http://stats.espncricinfo.com/ci/engine/stats/index.html"
#query = "?class=match_type;team=teamid;template=results;type=player_type"

def text(elt):
    x = None
    # print("--type ",type(elt))
    try:
        x = elt.text_content().replace(u'\xa0', u' ')
        tag_a = elt.find('a')
        
        if tag_a != None:
            player_id = tag_a.get('href')
            if player_id != None and 'player' in player_id:
                player_id = player_id.replace('/','_')
                x = x.replace(":"," ")
                x = x + ":" + player_id
                print("player link: ",x)
    except Exception as e:
        print("ERROR_2: ",e)
        x = ""
    return x

def getTableData(cid, tid, player_type, page_number):
    url = base_url + "?" + "class=" + str(cid) + ";page=" + str(page_number) + ";team=" + str(tid) + ";template=results;type=" + str(player_type)
    print(url)
    r = requests.get(url)
    root = lh.fromstring(r.content)

    for table in root.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[3]'):
        try:
            header = [text(th) for th in table.xpath('//th')]        # 1
            data = [[text(td) for td in tr.xpath('td')]  
                    for tr in table.xpath('//tr')]                   # 2
            data = [row for row in data if len(row)==len(header)]    # 3 
            data = pd.DataFrame(data, columns=header)                # 4
            print(data)
            # print(data.columns)
        except:
            print("ERROR: ",cid," -- ",player_type)
            pass


for i in range(1, team_ids+1):
    for ptype in player_type:
        for cid in range(1, match_type_ids+1):
            for page in range(1, pages+1):
                getTableData(cid,i,ptype,page)
                a = input()


# getData()