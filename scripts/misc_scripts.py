import collections
import json
def clean_coins():
    x = open("res/txt_corp/coin_list_clean_sorted.json","w+")
    coin_list=json.load(x)
    coin_list_sorted=collections.OrderedDict(sorted(coin_list.items()))
    json.dump(coin_list_sorted, x, indent=4, separators=(',', ': '), ensure_ascii="false")
    x.close()