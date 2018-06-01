import json

def clean_ambiguous_coins():
    PATH_COIN_LIST='../res/txt_corp/coin_list.json'
    PATH_AMB_COINS='../res/txt_corp/ambiguous_coins.txt'

    with open(PATH_COIN_LIST)as f:
        coin_dict = json.load(f)
        f.close()

    with open(PATH_AMB_COINS) as f:
        amb=f.read()
        amb=amb.split(sep="\n")
        coin=[]

        for word in amb:
            x = word.split(sep=",")

            coin.append(x)

    for item in coin:
        x="None"
        print(item)
        if item[1]==" None":
            item[1]=""

    for item in coin:
        for key, value in coin_dict.items():
            if key == item[0]:
                print(" found" )
                if len(item)>2:
                    coin_dict[key]=[item[1].strip(),item[2].strip()]
                else:
                    coin_dict[key] = [item[1].strip()]
    print(coin_dict)

    f = open("../res/txt_corp/coin_list_clean.json","w+")
    json.dump(coin_dict, f, indent=4, separators=(',', ': '), ensure_ascii=False)
    f.close()

clean_ambiguous_coins()