import json
import io
import tokenizer
import numpy as np

from os import listdir
from os.path import isfile, join
from  MysqlConnector import  MysqlConnector



def open_file(f_name):
    print("File opened"+f_name)
    with io.open(f_name,'r',encoding="utf-8") as f:
        text=f.read()
    return text

def write_file(f_name,some_list):
    with io.open(f_name, 'w', encoding="utf-8") as f:
        json.dump(some_list, f, ensure_ascii=False)

def search_for_coins(ids, save_origin_word=False,from_db=False,):

    msqlc = MysqlConnector()
    PATH_COIN_LIST='../res/txt_corp/coin_list_clean.json'
    PATH_OUTPUT='../res/txt_corp/technical_words.json'

    if save_origin_word:
        PATH_OUTPUT="../res/txt_corp/technical_words_with_origin.json"

    technical_words = {}

    with open(PATH_COIN_LIST)as f:
        coin_dict=json.load(f)

    for i in ids:

        tags = []
        text=""
        if not from_db:
            text = open_file("../res/main_txt/rss_entries/txt-" + str(i) + ".txt")  # for rss_entries
        else:
            text=""
            pass

        text = tokenizer.lemmatize(text)

        print(text)

        for word in text:

            for k, v in coin_dict.items():

                if len(v) == 1:
                    if word == v[0]:
                        tags.append(k)
                        print(word, "        ", k, v)
                        continue
                else:
                    if word == v[0] or word.lower() == v[1].lower():
                        print(word, "        ", k, v)
                        if save_origin_word:
                            tags.append([word, v[1]])
                            continue

                        else:
                            tags.append(v[1])
                            continue

        technical_words["txt-" + str(i)] = tags

    #Save File to PATH_OUTPUT
    f = open(PATH_OUTPUT, "w+")
    json.dump(technical_words, f, indent=4, separators=(',', ': '), ensure_ascii="false")
    f.close()


def main():

    mypath = "../res/main_txt/rss_entries"
    onlyfiles = [int(f[4:-4]) for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles = sorted(onlyfiles)

    # GETting actual file names from folder

    FILES_IDS = onlyfiles
    search_for_coins(FILES_IDS)

if __name__ == '__main__':
    main()