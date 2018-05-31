import json
import io
import tokenizer
import numpy as np

from os import listdir
from os.path import isfile, join




def open_file(f_name):
    print("File opened"+f_name)
    with io.open(f_name,'r',encoding="utf-8") as f:
        text=f.read()
    return text

def write_file(f_name,some_list):
    with io.open(f_name, 'w', encoding="utf-8") as f:
        json.dump(some_list, f, ensure_ascii=False)

def search_for_coins(ids, save_origin=False):
    with open('../res/txt_corp/coin_list_clean.json')as f:
        coin_dict=json.load(f)
    technical_words = {}

    for i in ids:
        tags_words = []
        text = open_file("../res/main_txt/rss_entries/txt-" + str(i) + ".txt")  # for rss_entries
        text = tokenizer.lemmatize(text)
        print(text)
        for word in text:

            for k, v in coin_dict.items():

                if len(v) == 1:
                    if word == v[0]:
                        tags_words.append(k)
                        print(word, "        ", k, v)
                        continue
                else:
                    if word == v[0] or word.lower() == v[1].lower():

                        if save_origin:
                            tags_words.append([word, v[1]])
                        else:
                            tags_words.append(v[1])
                        print(word, "        ", k, v)
                        continue


            technical_words["txt-" + str(i)] = tags_words

        f_name = "../res/txt_corp/technical_words.json"
        if save_origin:
            f_name="../res/txt_corp/technical_words_with_origin.json"
        f = open(f_name, "w+")

        json.dump(technical_words, f, indent=4, separators=(',', ': '), ensure_ascii="false")
        f.close()


def main():
    mypath = "../res/main_txt/rss_entries"
    onlyfiles = [int(f[4:-4]) for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles = sorted(onlyfiles)

    some_list = []

    # GETting actual file names from folder
    AMOUNT_OF_FILES = onlyfiles
    search_for_coins(AMOUNT_OF_FILES,save_origin=True)





if __name__ == '__main__':
    main()