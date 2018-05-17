import nltk
import io
import re
text=""
new_text=[]
new_string=""
f_name = "Binance Flash Update!"
f_name = "../main_text/" + f_name + ".txt"

with io.open(f_name, "r", encoding="utf-8") as f:
    text = f.read()
print(text)
# removing links
# slabo dziala re_pattern_link ='/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g'
re_pattern_link_new='(www|http:|https:)+[^\s]+[\w]'
#po_re = re.search(re_pattern_link,text)
#print(po_re)

po_re =re.search(re_pattern_link_new,text)
po_re_many = re.findall(re_pattern_link_new,text)
print(po_re_many)
print(po_re.group(0))
# for i,v  in enumerate(po_re_many):
    # print(po_re_many.group(i))
# text =text.__repr__()
# print(text)
# test = text.split(sep = ' ')
# print(test)

#remove not digit not alhaphbets words:
# for char in text:
#     #print(char, char.isalnum())
#     if not char.isalnum():
#         char = " "
#     new_text.append(char)
#
# new_string=''.join(new_text)
#
# words = new_string.split(sep=" ")
# #for word in words:
#     #print(word)
#
# for i,word in enumerate(words):
#     print(word, end=" ")
#     if i%10==0:
#         print("\n")