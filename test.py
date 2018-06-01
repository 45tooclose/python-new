from os import listdir
from os.path import isfile, join
from collections import Counter
from collections import OrderedDict
import json
with open("res/txt_corp/technical_words.json") as f:
    tech_dict = json.load(f)


with open("res/txt_corp/coin_list_clean.json") as f:
    coin_list = json.load(f)


freq_tech={}
unique_coins=[]
Counter =Counter()
#Adds counter for coin appearance in text for tech_dict
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

#Finds Unique coins in freq_tech
for k,v in freq_tech.items():

    for item in v:
        # print(k,v)
        if item not in unique_coins:
            unique_coins.append(item)

unique_coins= sorted(unique_coins)

#prints coins and theirs symobols that are found in unique coins_list
for item in unique_coins:
    for k,v in coin_list.items():
        if item==k:
            print(item,v)
            continue

for k,v in freq_tech.items():
    # print("---")
    for item,amount in v.items():
        # print(item,amount)
        Counter[item]+=amount

print(Counter)

for k,v in Counter.items():
    for coin,names in coin_list.items():
        if k==coin:
            print(coin,names,v)