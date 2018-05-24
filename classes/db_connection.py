import mysql.connector
import json
import datetime
import io
import datetime
from TextCleaner import TextCleaner

import pprint
from mysql.connector import errorcode

"""
ABANDONED, DONT USE
"""
class DBConnection:
    # CONFIG TO ACCESS TABLES
    db_config = {
        # DEFAULT
        'default': 'rss_medium_sample',
        'structure data': 'structured_data',
        'article base': 'article_base',
        'rss medium': 'rss_medium'
    }
    table_config = {
        'table':'',
        'column':'',
        'where':'',
        'limit':''
    }
    # GET CONNECTION CONFIG FROM FILE
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

        if table_name is None: table_name = self.db_config['default']
        if db_name is None: db_name = self.db_config['article base']

        query = " SELECT `COLUMN_NAME` "
        query += "FROM `INFORMATION_SCHEMA`.`COLUMNS` "
        query += "WHERE `TABLE_SCHEMA`='" + db_name + "'"
        query += "AND `TABLE_NAME`='" + table_name + "';"
        column_names = []

        self.execute_query(query)

        # Creating list
        for item in self.cursor:
            column_names.append(''.join(item))

        # Returns list
        return column_names

    """
    GETTING JSON RAW FILE FROM DB
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
    """
    def get_raw_json(self, table_name=None, column_name=None, return_dic=None, return_pos=None,where=None):

        if table_name is None:
            table_name = self.db_config['default']
        if column_name is None:
            column_name = self.db_config['json']
        if return_dic is None:
            return_dic = False
        if  where is None:
            where = '1'

        self.execute_query(self.select_query(table_name=table_name, column_name=column_name,where=where))
        row = self.cursor.fetchone()

        for item in row:
            json_dic = json.loads(''.join(item))

        json_list = []
        keys = ['topic', 'link_hub', 'links', 'time_created', 'tags', 'author', 'summary']
        json_dic_val = dict.fromkeys(keys)

        # TODO do refactoringu  dla json_list
        json_dic_list = ['id',
                         'title',
                         ['title_detail', 'base'],
                         'link',
                         'published_parsed',
                         ['tags', 'term'],
                         'author',
                         'summary']

        # TODO zmienic for item in json_dic_list żeby bral bezposrednio z listy a nie z ifow

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
            for key, value in json_dic_val.items():
                json_dic_val[key] = json_list[ite]
                ite += 1

        if return_dic:
            return json_dic_val
        else:
            if return_pos is None:
                return json_list
            else:
                return json_list[return_pos]

    def select_query(self, table_name, column_name=None, limit='1', where=''):
        if column_name is None:
            column_name = '*'
        if table_name is None:
            table_name = self.db_config['default']

        query = "SELECT " + column_name + " "
        query += "FROM " + table_name + " "
        query += "LIMIT" + limit + " "
        query += "WHERE" + where + ";"
        return query

    def get_rss_medium_sample_vals(self):

        query = self.select_query(table_name='rss_medium_sample', column_name='*', limit='1')
        self.execute_query(query)
        row = self.cursor.fetchone()

        keys = ['id_rss_medium', 'html', 'main_text']
        sql_dic = dict.fromkeys(keys)
        sql_dic['id_rss_medium'] = row[0]

        # sql_dic_val['html'] = row[4] # OPTIONAL
        sql_dic['main_text'] = row[5]

        return sql_dic

    def get_value_from_row(self,table,column,limit= None):

        if limit is None:
            limit ='1'

        query=self.select_query(table_name=table,column_name=column,limit=limit)
        self.execute_query(query)
        row=self.cursor.fetchone()

        return row[0]

    # GET text from rss_medium_sample,
    # RETURN FILE with text
    def get_rss_medium_sample_text(self):

        query = self.select_query(table_name='rss_medium_sample', column_name='text', limit='1')
        self.execute_query(query)
        row = self.cursor.fetchone()
        tc = TextCleaner(txt=row[0])
        tc.clear_text()
        return tc.get_text()

    # CONVERTING JSON FILES TO INSERT_SQL QUERY
    def json_dic_to_sql(self, json_dic, sql_dic=None):

        list_of_columns = self.get_column_names(table_name='structured_data')
        sql_l = []
        list_of_none_columns = ['id_structured_data', 'id_rss_medium', 'main_text', 'html', 'date_created']

        for inum, val_c in enumerate(list_of_columns):
            if val_c in list_of_none_columns:
                sql_l.append(None)
            for key, val_d in json_dic.items():
                if val_c == key:
                    sql_l.append(val_d)
                    break

        if sql_dic:
            sql_l[1] = sql_dic['id_rss_medium']
            sql_l[5] = sql_dic['main_text']
            if sql_dic['html']:
                sql_l[9] = sql_dic['html']
            # TODO

        return sql_l

    def insert_query(self,values, query=None, table=None, ):
        # Get Column names from table
        if table is None:
            table = 'structured_data'
        columns = self.get_column_names(table_name=table)
        print(columns)
        if query is None:
            pass

        query = " INSERT INTO "
        query += "`" + table + "` ("
        for i, value in enumerate(columns):
            if i == columns.__len__() - 1:
                query += "`" + columns[i] + "`)"

            else:
                query += "`" + columns[i] + "`,"
        query += "VALUES("

        for i, val in enumerate(values):
            if i == 11:
                query += 'default'
            elif i == 10:
                query += 'null'
            elif val is None:
                print('null')
                query += 'null'
            elif type(val) is int:
                print('int')
                query += str(val)
            elif type(val) is datetime.datetime:
                print('datetime')
                query += "'" + str(val) + "'"
            elif type(val) is str:
                query += " '" + val + "' "
                print('str')

            if i == columns.__len__() - 1:
                query += ")"
            else:
                query += ", "
        self.execute_query(query)

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

    def create_values(self,i):

        json_dic=self.get_raw_json(column_name='json',return_dic=True)
        sql_dic = self.get_rss_medium_sample_vals()
        sql_dic['main_text'] =self.get_rss_medium_sample_text()
        values =  self.json_dic_to_sql(json_dic=json_dic,sql_dic=sql_dic)

        return values
    # def update_table_config(self,table=None,column=None,where=None,limit=None):
    #     self.table_config

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
    values =db.create_values()
    db.insert_query(values)



if __name__ == "__main__":
    main()
