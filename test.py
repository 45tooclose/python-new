f_name = None
loc = "../res/main_text/"
iterator =1

if f_name is None:
    f_name = "txt-" + str(iterator) + ".txt"
    if loc is not None:
        f_name = loc + f_name+1

print(f_name)
