import mysql.connector
import json
import datetime
import pprint
from mysql.connector import errorcode


class DBConnection:
    # CONNECTION CONFIG IN connection_config.txt
    # CONFIG TO ACCESS TABLES
    db_config = {
        # DEFAULT
        'default': 'rss_medium_sample',
        'article base': 'article_base',
        'rss medium': 'rss_medium'
    }

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

        if table_name is None: table_name = self.db_config['table']
        if db_name is None: db_name = self.db_config['article base']

        query = " SELECT `COLUMN_NAME` "
        query += "FROM `INFORMATION_SCHEMA`.`COLUMNS` "
        query += "WHERE `TABLE_SCHEMA`='" + db_name + "'"
        query += "AND `TABLE_NAME`='" + table_name + "';"
        column_names = []

        self.execute_query(query)

        for item in self.cursor:
            print(item)

        for item in self.cursor:
            column_names.append(''.join(item))

        # Returns list
        return column_names

    # GETTING JSON RAW FILE FROM DB
    # RETURNS LIST
    def get_raw_json(self, table_name=None, column_name=None):

        if table_name is None: table_name = self.db_config['table']
        if column_name is None: column_name = self.db_config['json']

        print(column_name)

        query = "SELECT " + column_name + " "
        query += "FROM " + table_name + " "
        query += "LIMIT 1 "

        print(query)

        self.execute_query(query)
        row = self.cursor.fetchone()

        for item in row:
            json_dic = json.loads(''.join(item))

        json_list = []

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
        #TEST
        # Check the json_list without 'summary' and it's length
        # pprint.pprint(json_list[0:6])
        # print(json_list.__len__())

        return json_list

    # CONVERTING JSON FILES TO INSERT_SQL QUERY
    def json_to_sql_values(self, json_dic):
        print("hyy")
    #
    # TODO INSERTING TO TABLE
    def insert_query(self, query=None, table=None):

        #Get Column names from table
        if table is None:
            columns = self.get_column_names(table_name='structured_data')
        else:
            columns = self.get_column_names(table_name=table)
        #print(columns)

        #query_temp = "INSERT INTO `" + table + "`("
        for item in columns:
            print(item)

        query = """  INSERT INTO
        `structured_data`(`id_structured_data`, 
        `id_rss_medium`, 
        `time_created`, 
        `topic`,
        `author`, 
        `main_text`, 
        `tags`,
        `links`, 
        `link_hub`,
        `html`,
        `summary`)
        VALUES(
        null,
         124,
        '2011-06-06 13:15:20',
        'raz',
        'peja',
        'dlugitext',
        'tekst,teskt',
        'http://ayy.com',
        'szto',
        '<html></html>', 
        'traeszakfg'
        )
        ;    
        """
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
            print("sucess.")
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
    print("in main")
    db = DBConnection()

    # column_names= db.get_column_names(table_name='rss_medium_sample')
    db.insert_query('')
    # db.get_raw_json(column_name="json")


if __name__ == "__main__":
    main()
