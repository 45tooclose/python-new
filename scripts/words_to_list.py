import json
import io
import tokenizer
import numpy as np
from nltk.corpus import wordnet
some_list=[]

def open_file(f_name):
    print("File opened")
    with io.open(f_name,'r',encoding="utf-8") as f:
        text=f.read()
    return text

def write_file(f_name):
    with io.open(f_name, 'w', encoding="utf-8") as f:
        json.dump(some_list, f, ensure_ascii=False)


def main():
    for i in np.arange(1,15,1):
        text = open_file("../res/main_txt/rss_entries/txt-"+str(i)+".txt") #for rss_entries
        text = tokenizer.lemmatize(text)
        print(text)

if __name__ == '__main__':
    main()