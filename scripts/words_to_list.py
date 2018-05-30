import json
import io
import tokenizer
import numpy as np
some_list=[]

def open_file(f_name):
    print("File opened"+f_name)
    with io.open(f_name,'r',encoding="utf-8") as f:
        text=f.read()
    return text

def write_file(f_name,some_list):
    with io.open(f_name, 'w', encoding="utf-8") as f:
        json.dump(some_list, f, ensure_ascii=False)


def main():

    with open('../res/txt_corp/coin_list_clean.json')as f:
        coin_dict=json.load(f)
        f.close()
    technical_words={}

    for i in np.arange(1,15,1):
         tags_words = []
         text = open_file("../res/main_txt/rss_entries/txt-"+str(i)+".txt") #for rss_entries
         text = tokenizer.lemmatize(text)
         print(text)
         for word in text:

            for k, v in coin_dict.items():
                if word == v[0]:
                    tags_words.append(v[1])
                    print(word,"        ",k,v)
                elif v[1]:
                    if word.lower() == v[1].lower():
                        tags_words.append(v[1])

         technical_words["txt-"+str(i)]=tags_words


    for i in technical_words:
        print(i)

    f=open("../res/txt_corp/technical_words.json","w+")
    json.dump(technical_words, f, indent=4, separators=(',', ': '),ensure_ascii="false")
    f.close()

if __name__ == '__main__':
    main()