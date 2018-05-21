
# coding: utf-8

# In[1]:


import io
import re


# In[10]:


text = ""
f_name = "../res/main_txt/Binance Flash Update!.txt"
try:
    f = io.open(f_name,"r",encoding="utf-8")
    text = f.read()
except FileNotFoundError:
    print("File Not Found")
else:
    f.close()


# In[11]:


print(text)


# In[12]:


# pattern for detecting binded words 'XXYy' splitting them
re_pattern_split ='(([A-Z]+([a-z])))'
re_matches_split =re.findall(re_pattern_split,text)
for match in re_matches_split:
    if match[0].__len__()  > 2:
      #  print(match[0])
        fixed_match=match[0][:-2]+" "+match[0][-2:]
        text= text.replace(match[0],fixed_match)
print(text)


# In[13]:


# pattern for detecting binded words 'yyyXx' splitting them
re_pattern_split ='(([a-z])+([A-Z]))'
re_matches_split =re.findall(re_pattern_split,text)
for match in re_matches_split:
        fixed_match=match[0][:-1]+" "+match[0][-1]
        text= text.replace(match[0],fixed_match)
print(text)


# In[14]:


#Detection of links

# pattern for main site names 2
re_pattern_2='(http|ftp|https)\:\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
re_match = re.findall(re_pattern_2,text)
links_list=[]
for match in re_match:
    # print(match[0],match[1],match[2])
    match_str=''.join(match[0])+'://'
    match_str+=''.join(match[1])
    match_str+=''.join(match[2])
    text=text.replace(match_str," ")
    links_list.append(match_str)
print(text)
for v in links_list:
    print(v)

print(text)
# In[15]:


#check if elements exists in list
def is_unqiue(element,u_set):
    if element in u_set:
        return False
    else:
        return True


# In[16]:


# Finding special characters
not_alnum=[]
for char in text:
    if not char.isalnum() and not char.isspace():
        # print(char, char.isalnum(), char.isspace())
        if not char in not_alnum:
            not_alnum.append(char)
        else:
            pass
print(not_alnum)


# In[17]:


#looking for dates using regex
re_pattern_date='(([0-9]{2,4})(\/|\-|\s)([0-9]{1,2})(\/|\-|\s)([0-9]{1,4}))'
re_match = re.findall(re_pattern_date,text)

dates_list=[]
for match in re_match:
    dates_list.append(match[0])
    text=text.replace(match[0]," ")
print(text)

