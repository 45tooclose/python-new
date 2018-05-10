import pprint
connection_config = {
    'user': 'root',
    'password': 'None',
    'host': '127.0.0.1',
    'database': 'article_base'
}
# with open('workfile.txt','w') as f:
#
#         for k,v in connection_config.items():
#             f.write(k+ " ")
#            # print(k)
#             f.write(v+ "\n")
#            # print(v)

with open('connection_config.txt','r') as f:
    read_data=[]
    for line in f:
        for word in line.split():
            if word == 'None':
                read_data.append('')
            else:
                read_data.append(word)


connection_config = dict(zip(read_data[::2], read_data[1::2]))
pprint.pprint(connection_config)