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



        #json_list=

        json_list = []
        # print("title:"+json_dic['title'])
        json_list.append(json_dic['title'])

        # print("title_details:"+json_dic['title_detail']['base'])
        json_list.append(json_dic['title_detail']['base'])

        # print("link:"+json_dic['link'])
        json_list.append(json_dic['link'])

        time_list=[]
        for item in json_dic['published_parsed'][0:6]:
            time_list.append(item)
        # print(time_list)
        date_published =datetime.datetime(*map(int,time_list))
        # print(date_published)
        json_list.append(date_published)

        tags_list=[]
        for item in json_dic['tags']:
            tags_list.append(item['term'])
        # print(tags_list)
        json_list.append(tags_list)

        # print("author:"+json_dic['author'])
        json_list.append(json_dic['author'])

        # print("summary:"+json_dic['summary'])
        json_list.append(json_dic['summary'])

        pprint.pprint(json_list[0:6])
        #print(json_list.__len__())
        return json_list

    #CONVERTING JSON FILES TO INSERT_SQL QUERY
    def json_to_sql_values(self,json_dic):
        sql_values = []

        #TODO REFACTORING
        # a="text"
        # b="content"
        # c="data"

        sql_values.append(json_dic["id"])
        sql_values.append(json_dic["text"]["content"]["data"]["username"])
        sql_values.append(json_dic["text"]["content"]["data"]["text"])
        sql_values.append(datetime.strptime(json_dic["text"]["content"]["data"]["time"], "%a %b %d %H:%M:%S %Y %Z"))
        sql_values.append(json_dic["text"]["channel"])
        sql_values.append(json_dic["text"]["content"]["data"]["room_id"])
        sql_values.append(json_dic["text"]["content"]["data"]["symbol"])
        sql_values.append(json_dic["text"]["content"]["data"]["user_id"])



        return sql_values

    #TODO INSERTING TO TABLE
    def insert_into_table(self,sql_values, columns="",table_name=None):

        if columns=="":
            columns= self.get_column_names()

        if table_name is None:
            table_name  = self.db_config['table']
        # print(sql_values)
        # print(columns)

        for (i,item) in enumerate(sql_values):

             if not isinstance(item,str) and not isinstance(item,datetime):
                 sql_values[i]= str(item)

        for item in sql_values:
            print(type(item))

        # toString = ",".join(sql_values)
        # print(toString)

        query = "INSERT INTO "+table_name+" "
        #KOLUMNY
        #query +="("+columns+") "
        query +="VALUES(" + sql_values[0] + ")"
        print(query)

        # try:
        #     self.cursor.execute(query)
        #     self.cnx.commit()
        #     print("COMMITED")
        # except:
        #     self.cnx.rollback()
        #     print("ROLLBACK")

    #TODO CREATING QUERY
    # BROKEN DONT USE
    def create_query(self):
        self.query = input("Insert MySQL query")
        print(self.query)
        self.cursor.execute(self.query)
        for a in self.cursor:
            answer_arr = json.lods(''.join(a))
        self.query = answer_arr

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

    #OLD DONT USE
    #OPENNING CONNECTION TO DB
    #USE CONNECTION_CONFIG TO CHANGE VARS
    # def connect_to_db(self):
    #
    #     try:
    #         cnx = mysql.connector.connect(**self.connection_config)
    #
    #     except mysql.connector.Error as err:
    #         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #             print("Something is wrong with your user name or password")
    #         elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #             print("Database does not exist")
    #         else:
    #             print(err)
    #
    #     else:
    #         print("mysql connected")
    #         cursor = cnx.cursor()
    #         print("cursor created")
    #
    #         raw_json_val = self.get_raw_json()
    #         print(raw_json_val)
    #
    #         # TEST
    #         # for item in cursor
    #
    #         cursor.close()
    #         print("cursor closed")
    #         cnx.close()

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
