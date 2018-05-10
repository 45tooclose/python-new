import mysql.connector
import json
import datetime
import pprint
from mysql.connector import errorcode


class DBConnection:

    #CONNECTION CONFIG IN connection_config.txt
    #CONFIG TO ACCESS TABLES
    db_config={
        #DEFAULT
        'table': 'rss_medium_sample',
        'article_base': 'article_base',
        'rss_medium': 'rss_medium'


    }


    def get_connection_config(self,loc):
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

    #GET COLUMNS FROM TABLE
    #RETURNS LIST
    def get_column_names(self,table_name=None,db_name=None):
        print("in get_column_names")

        if table_name is None:
            table_name=self.db_config['table']
        if db_name is None:
            db_name=self.db_config['article_base']

        query = " SELECT `COLUMN_NAME` "
        query += "FROM `INFORMATION_SCHEMA`.`COLUMNS` "
        query += "WHERE `TABLE_SCHEMA`='"+db_name+"'"
        query += "AND `TABLE_NAME`='"+table_name+"';"
        column_names = []

        self.execute_query(query)

        for item in self.cursor:
            print(item)

        for item in self.cursor:
            column_names.append(''.join(item))

        #Returns list
        return column_names

    #GETTING JSON RAW FILE FROM DB
    #RETURNS DICTIONARY
    def get_raw_json(self, table_name=None, column_name=None):

        if table_name is None: table_name = self.db_config['table']
        if column_name is None: column_name =self.db_config['json']

        print(column_name)

        query = "SELECT "+column_name+" "
        query += "FROM "+table_name+" "
        query += "LIMIT 1 "

        print(query)

        self.execute_query(query)
        row = self.cursor.fetchone()

        for item in row:
            json_dic =json.loads(''.join(item))

        json_list = []

        json_list.append(json_dic['title'])

        json_list.append(json_dic['title_detail']['base'])

        json_list.append(json_dic['link'])

        time_list=[]
        for item in json_dic['published_parsed'][0:6]:
            time_list.append(item)
        date_published =datetime.datetime(*map(int,time_list))
        json_list.append(date_published)

        tags_list=[]
        for item in json_dic['tags']:
            tags_list.append(item['term'])
        tags_str=','.join(tags_list)
        json_list.append(tags_str)

        json_list.append(json_dic['author'])

        json_list.append(json_dic['summary'])

        #Check the json_list without 'summary' and it's length
        #pprint.pprint(json_list[0:6])
        #print(json_list.__len__())
        
        return json_list

    #CONVERTING JSON FILES TO INSERT_SQL QUERY
    def json_to_sql_values(self,json_dic):
        print("hyy")

    #TODO INSERTING TO TABLE
    def insert_into_table(self,sql_values, columns="",table_name=None):
        print("temp")

    #TODO CREATING QUERY
    # BROKEN DONT USE
    def create_query(self):
        print("benis")

    #EXECUTIN QUERY
    def execute_query(self, query=""):
        if query=="":
            query = self.query
        print("executing")
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            print("sucess.")
        except:
            self.cnx.rollback()
            print("failure.")



    def __init__(self):
        self.connection_config = self.get_connection_config('../connection_config.txt')
        self.cnx = mysql.connector.connect(**self.connection_config)
        self.cursor = self.cnx.cursor(buffered =True)
        self.query = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cnx:
            self.cnx.close()

def main():
    print("in main")
    db = DBConnection()

    #column_names= db.get_column_names(table_name='rss_medium_sample')

    db.get_raw_json(column_name="json")


if __name__ == "__main__":
    main()
