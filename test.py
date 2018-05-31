from os import listdir
from os.path import isfile, join
from collections import Counter

import json
with open("res/txt_corp/technical_words.json") as f:
    tech_dict = json.load(f)


with open("res/txt_corp/coin_list_clean.json") as f:
    coin_list = json.load(f)





freq_tech={}
unique_coins=[]

for k,v in tech_dict.items():

    if len(v)==0:
        continue
    else:
        cnt = {}
        for item in v:
            if item not in cnt.keys():
                cnt.update({item:1})
            else:
                cnt[item]+=1


    freq_tech.update({k:cnt})



for k,v in freq_tech.items():
    for item in v:
        if item not in unique_coins:
            unique_coins.append(item)
unique_coins= sorted(unique_coins)

for item in unique_coins:
    for k,v in coin_list.items():
        if item==k:
            # print(item,v)
            continue
