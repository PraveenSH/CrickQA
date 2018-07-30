import os
import sys
import collections
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import lxml.html as lh
import requests
import pickle

team_ids = 10
match_type = ["test", "odi", "t20"]
match_type_ids = 3
pages = 5
player_type = ["batting", "bowling", "fielding", "partnership", "team"]
venue = 3
base_url = "http://stats.espncricinfo.com/ci/engine/stats/index.html"
name_to_id = {}


def parse_url(cid, tid, player_type, page_number, flag):
    url = base_url + "?" + "class=" + str(cid) + ";page=" + str(page_number) + ";team=" + str(
        tid) + ";template=results;type=" + str(player_type)
    r = requests.get(url)
    root = lh.fromstring(r.content)

    for table in root.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[3]'):
        try:
            if flag == 'id':
                data = [[index_player_id_list(td) for td in tr.xpath('td')]
                        for tr in table.xpath('//tr')]
            if flag == 'name':
                data = [[index_player_name_list(td) for td in tr.xpath('td')]
                        for tr in table.xpath('//tr')]
        except:
            print("ERROR: ", cid, " -- ", player_type)
            pass


def index_player_id_list(elt):
    x = None
    try:
        x = elt.text_content().replace(u'\xa0', u' ')
        tag_a = elt.find('a')

        if tag_a != None:
            player_id = tag_a.get('href')
            if player_id != None and 'player' in player_id:
                pid = player_id.split('/')[-1].split('.')[0]
                print(pid, str(x))
                name_to_id[x] = int(pid)
                pickle.dump(name_to_id, open("../Mappings/player_to_id.pkl", 'w'))
    except Exception as e:
        print("ERROR_2: ", e)

def index_player_name_list(elt):
    x = None
    try:
        x = elt.text_content().replace(u'\xa0', u' ')
        tag_a = elt.find('a')

        if tag_a != None:
            player_id = tag_a.get('href')
            if player_id != None and 'player' in player_id:
                player_url = "http://www.espncricinfo.com"+player_id

                #name_to_id[x] = str(x)
                #pickle.dump(name_to_id, open("../Mappings/nick_name_to_player.pkl", 'w'))
    except Exception as e:
        print("ERROR_2: ", e)

def index_player_ids():
    for i in range(1, team_ids + 1):
        for ptype in player_type:
            for cid in range(1, match_type_ids + 1):
                for page in range(1, pages + 1):
                    parse_url(cid, i, ptype, page, 'id')

def index_player_nick_names():
    for i in range(1, team_ids + 1):
        for ptype in player_type:
            for cid in range(1, match_type_ids + 1):
                for page in range(1, pages + 1):
                    parse_url(cid, i, ptype, page, 'name')
                    input()
index_player_nick_names()