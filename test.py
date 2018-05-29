json_dic={'id': "id value",
          'title': "title vlaue",
            'title_detail' : ["one","two"],
            'link': "link value",
            'published_parsed':" parssed value",
            'tags': {'term':"raz"},
            'author': 'heh',
            'summary': "summary"}



json_dic_list = ['id',
                 'title',
                 ['title_detail', 'base'],
                 'link',
                 'published_parsed',
                 ['tags', 'term'],
                 'author',
                 'summary']


for v in json_dic_list:
    if type(v) is list:
        print ("list",v)
    else:
        print(v)