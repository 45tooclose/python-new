import json

black_dict=dict
amb_dict=dict

with open('res/txt_corp/coin_list.json')as f:
    coin_dict = json.load(f)
    f.close()

with open('res/txt_corp/ambiguous_coins.txt') as f:
    amb=f.read()
    amb_split=amb.split(sep="\n")
    tmp_list=[]
    for word in amb_split:
        x = word.split(sep=",")
        tmp_list.append(x)

for item in tmp_list:
    x="None"
    if item[1]==" None":
        item[1]=""

for item in tmp_list:
    for key,value in coin_dict.items():
        if key==item[0]:
            print(" found" )
            coin_dict[key]=[item[1].strip()]
print(coin_dict)

f = open("res/txt_corp/coin_list_clean.json","w+")

json.dump(coin_dict, f, indent=4, separators=(',', ': '), ensure_ascii=False)

f.close()
