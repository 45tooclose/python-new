import mysql.connector
import json
import datetime
import io
import datetime
import pprint
from mysql.connector import errorcode


class DBConnection:

    # CONFIG TO ACCESS TABLES
    db_config = {
        # DEFAULT
        'default': 'rss_medium_sample',
        'structure data': 'structured_data',
        'article base': 'article_base',
        'rss medium': 'rss_medium'
    }
    #GET CONNECTION CONFIG FROM FILE
    # CONNECTION CONFIG IN connection_config.txt
    def get_connection_config(self, loc):
        with open(loc, 'r') as f:
            read_data = []
            for line in f:
                for word in line.split():
                    if word == 'None':
                        read_data.append('')
                    else:
                        read_data.append(word)
        connection_config = dict(zip(read_data[::2], read_data[1::2]))
        return connection_config

    # GET COLUMNS FROM TABLE
    # RETURNS LIST
    def get_column_names(self, table_name=None, db_name=None):
        print("in get_column_names")

        if table_name is None: table_name = self.db_config['default']
        if db_name is None: db_name = self.db_config['article base']

        query = " SELECT `COLUMN_NAME` "
        query += "FROM `INFORMATION_SCHEMA`.`COLUMNS` "
        query += "WHERE `TABLE_SCHEMA`='" + db_name + "'"
        query += "AND `TABLE_NAME`='" + table_name + "';"
        column_names = []

        self.execute_query(query)

        #Creating list
        for item in self.cursor:
            column_names.append(''.join(item))

        # Returns list
        return column_names

    # GETTING JSON RAW FILE FROM DB
    # args:
    # table_name - name of the table
    # column_name - name of column to retrive data
    # return_dic - if false will retrun list, else dictionary
    # RETURNS LIST OR DIC
    # json_list - json_dic_val:
    # 1 - topic
    # 2 - link_hub
    # 3 - link
    # 4 - time_created
    # 5 - tags
    # 6 - author
    # 7 - summary
    def get_raw_json(self, table_name=None, column_name=None,return_dic=None,return_pos=None):

        if table_name is None: table_name = self.db_config['default']
        if column_name is None: column_name = self.db_config['json']
        if return_dic is None: return_dic = False

        self.execute_query(self.select_query(table_name=table_name,column_name=column_name))
        row = self.cursor.fetchone()

        for item in row:
            json_dic = json.loads(''.join(item))

        json_list = []
        json_dic_val = {}
        keys = ['topic','link_hub','links','time_created','tags','author', 'summary']
        json_dic_val= dict.fromkeys(keys)

        #TODO do refactoringu  dla json_list
        json_dic_list = ['id',
                         'title',
                         ['title_detail','base'],
                         'link',
                         'published_parsed',
                         ['tags','term'],
                         'author',
                         'summary']


        #TODO zmienic for item in json_dic_list żeby bral bezposrednio z listy a nie z ifow


        json_list.append(json_dic['title'])
        json_list.append(json_dic['title_detail']['base'])
        json_list.append(json_dic['link'])

        time_list = []
        for item in json_dic['published_parsed'][0:6]:
            time_list.append(item)
        date_published = datetime.datetime(*map(int, time_list))
        json_list.append(date_published)

        tags_list = []
        for item in json_dic['tags']:
            tags_list.append(item['term'])
        tags_str = ','.join(tags_list)
        json_list.append(tags_str)

        json_list.append(json_dic['author'])
        json_list.append(json_dic['summary'])

        if return_dic == True:
            ite = 0
            for key,value in json_dic_val.items():
                json_dic_val[key]=json_list[ite]
                ite += 1
        # TEST
        # Check the json_list without 'summary' and json_list length
        #print.pprint(json_list[0:6])
        #print(json_list.__len__())
        # print(json_dic_val)
        if return_dic:
            return json_dic_val
        else:
            if return_pos is  None:
                return json_list
            else:
                return json_list[return_pos]

    def select_query(self,table_name,column_name=None,limit='1'):
        if column_name is None:
            column_name='*'
        if table_name is None:
            table_name = self.db_config['default']

        query = "SELECT " + column_name + " "
        query += "FROM " + table_name + " "
        query += "LIMIT"+limit+" ;"

        return query

    def get_rss_medium_sample_vals(self):
        query = self.select_query(table_name='rss_medium_sample',column_name='*',limit='1')
        self.execute_query(query)
        row = self.cursor.fetchone()
        sql_dic_val={}
        keys = ['id_rss_medium','html','main_text']
        sql_dic_val= dict.fromkeys(keys)
        sql_dic_val['id_rss_medium'] = row[0]

        # HTML OPTIONAL
        # sql_dic_val['html'] = row[4]

        sql_dic_val['main_text'] = row[5]
        return sql_dic_val

    #GET text from rss_medium_sample,
    #RETURN FILE with name of topic
    def get_rss_medium_sample_text(self,f_name=None):
        if f_name is None:
            now =datetime.datetime.now()
            f_name = now.strftime("%Y-%m-%d %H-%M")

        query = self.select_query(table_name='rss_medium_sample',column_name='*',limit='1')
        self.execute_query(query)
        row = self.cursor.fetchone()
        main_text=row[5]
        print(main_text)
        with io.open("../main_text/" + f_name + ".txt","w",encoding="utf-8") as f:
            f.write(main_text)

    # CONVERTING JSON FILES TO INSERT_SQL QUERY
    def json_dic_to_sql_values(self, json_dic,sql_dic=None):

        list_of_columns = self.get_column_names(table_name='structured_data')
        sql_l = []
        list_of_none_columns =['id_structured_data','id_rss_medium','main_text','html','date_created']
        for inum, val_c in enumerate(list_of_columns):
                if val_c in list_of_none_columns:
                    sql_l.append(None)
                for key, val_d in json_dic.items():
                        if val_c == key:
                            sql_l.append(val_d)
                            break
        if sql_dic != None:
            #sql_l[]
            print(sql_l)
            sql_l[1] = sql_dic['id_rss_medium']
            sql_l[5] = sql_dic['main_text']
            sql_l[9] = sql_dic['html']
            #TODO
        print(sql_l)

        return sql_l

    # TODO INSERTING TO TABLE
    def insert_query(self, query=None, table=None,values=None):
        #Get Column names from table
        if table is None:
            table='structured_data'
            columns = self.get_column_names(table_name=table)
        else:
            columns = self.get_column_names(table_name=table)

        #FIXME poprawic query
        query = " INSERT INTO "
        query += "`" + table + "` ("
        for i,value in enumerate(columns):
            if i == columns.__len__()-1:
                query += "`" + columns[i] + "`)"

            else:query += "`" + columns[i] + "`,"
        query +="VALUES("

        for i, val in enumerate(values):

            #print(type(val), val)
            if val is None:
                print('null')
                query+='null'
            elif type(val) is int:
                print('int')
                query+= str(val)
            elif type(val) is datetime.datetime:
                print('datetime')
                query+="'"+str(val)+"'"
            elif type(val) is str:
                query+=" '"+val+"' "
                print('str')

            if i ==columns.__len__()-1:
                query+= ")"
            else:
                query +=", "

            # if val=='None':
            #     val='null'
            #     query += " "+ val + " "
            # else:
            #     query += "`" + val + "`"
            #
            # if i == columns.__len__() - 1:
            #         query += " )"
            # else:
            #     query += ","

        with io.open("kek","w",encoding="utf-8") as f:
            f.write(query)
        # self.execute_query(query)
        # query +=`id_structured_data`,
        # query +=`id_rss_medium`,
        # query +=`time_created`,
        # query +=`topic`,
        # query +=`author`,
        # query +=`main_text`,
        # query +=`tags`,
        # query +=`links`,
        # query +=`link_hub`,
        # query +=`html`,
        # query +=`summary`)


        # query +=VALUES(
        # query += null,
        # query += 124,
        # query +='2011-06-06 13:15:20',
        # query +='raz',
        # query +='peja',
        # query +='dlugitext',
        # query +='tekst,teskt',
        # query +='http://ayy.com',
        # query +='szto',
        # query +='<html></html>',
        # query +='traeszakfg'
        #);
        #self.execute_query(query)

    # TODO CREATING QUERY
    def create_query(self):
        print("benis")

    # EXECUTIN QUERY
    def execute_query(self, query=""):
        if query == "":
            query = self.query
        print("executing")
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            print("success.")
        except mysql.connector.Error as err:
            print(self.cnx.rollback())
            print(err)
            print("failure.")

    def __init__(self):
        self.connection_config = self.get_connection_config('../connection_config.txt')
        self.cnx = mysql.connector.connect(**self.connection_config)
        self.cursor = self.cnx.cursor(buffered=True)
        self.query = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cnx:
            self.cnx.close()


def main():
    db = DBConnection()
    topic = db.get_raw_json(column_name='json',return_pos=0)
    db.get_rss_medium_sample_text(f_name=topic)
    # db.get_rss_medium_sample_vals()
    # column_names= db.get_column_names(table_name='rss_medium_sample')
    # db.insert_query()
    # json_dic = db.get_raw_json(column_name="json",return_dic=True)
    # sql_dic = db.get_rss_medium_sample_vals()

    # values = db.json_dic_to_sql_values(json_dic,sql_dic=sql_dic)
    # print(values[5])
    #db.insert_query(values=values)
if __name__ == "__main__":
    main()