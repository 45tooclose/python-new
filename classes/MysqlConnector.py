import mysql.connector
import json
import io
import datetime
import pprint
from TextCleaner import TextCleaner


class MysqlConnector:
    # FROM EXTERNAL FILE
    connection_config = {}

    # TABLES AND COLUMNS FROM connection_config['database']
    # todo refactor default value
    tables_config = {'default': 'structured_data'}

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

    def get_tables(self):

        database = self.connection_config['database']

        query = "SELECT TABLE_NAME "
        query += "FROM INFORMATION_SCHEMA.TABLES "
        query += "WHERE TABLE_TYPE = 'BASE TABLE' "
        query += "AND TABLE_SCHEMA = '" + database + "';"
        table_names = []

        self.execute_query(query)
        for item in self.cursor:
            table_names.append(''.join(item))
        return table_names

    def get_columns(self, table=None):

        if table is None:
            table = self.tables_config['default']
        db_name = self.connection_config['database']

        query = " SELECT `COLUMN_NAME` "
        query += "FROM `INFORMATION_SCHEMA`.`COLUMNS` "
        query += "WHERE `TABLE_SCHEMA`='" + db_name + "'"
        query += "AND `TABLE_NAME`='" + table + "';"
        column_names = []

        self.execute_query(query)

        # Creating list
        for item in self.cursor:
            column_names.append(''.join(item))

        # Returns list
        return column_names

    def get_tables_config(self):
        return self.tables_config

    def select_query(self, columns, table, limit=None, where=None):

        query = "SELECT " + columns + " "
        query += "FROM " + table + " "
        if where != None:
            query += "WHERE" + where + ""
        if limit != None:
            query += "LIMIT" + limit + ""
        query += ";"

        return query

    def execute_query(self, query="", returns=None):

        """
        Executes query
        Keyword arguments:

        Returns
        """
        if query == "":
            query = self.query
        print(query[0:20])
        print("executing")
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            print("success.")
        except mysql.connector.Error as err:
            print(self.cnx.rollback())
            print(err)
            print("failure.")

        if returns != None:
            print("fetching")
            rows = self.cursor.fetchall()
            return rows

        # TODO one column fix
    def insert_to_table(self, table, values, dictionary=False,one_column=None):
        """
        Inserting to table with values
        """
        columns = self.get_columns(table=table)

        if one_column is not None:
            if one_column in columns:
                columns=[one_column]
        query = " INSERT INTO "
        query += "`" + table + "` ("
        for i, value in enumerate(columns):
            if i == columns.__len__() - 1:
                query += "`" + columns[i] + "`)"
            else:
                query += "`" + columns[i] + "`,"
        query += "VALUES("

        if dictionary:

            match=False

            for i,column in enumerate(columns):
                match=False
                default_out='null'

                for key, value in values.items():
                    if match:
                        break
                    if column == key:
                        query +=  self.check_datatype(value)
                        match=True

                if match==False:
                    query+=default_out

                if i == columns.__len__() - 1:
                    query += ")"
                else:
                    query += ","
        else:
            for i, val in enumerate(values):
                query += self.check_datatype(val)
                if i == columns.__len__() - 1:
                    query += ")"
                else:
                    query += ", "
        #return(query)
        self.execute_query(query)

    def check_insert(self,query):
        pass

    def check_datatype(self,val):
        if val == 'default':
            val='default'
            return val
        elif val is None:
            val='null'
            return val
        elif type(val) is int:
            val=" '"+str(val)+"'"
            return val
        elif type(val) is str or datetime.datetime:
            val=" '" + val + "'"
            return val

    def init_tables_config(self):
        tables = self.get_tables()

        for table in tables:
            columns = self.get_columns(table)
            self.tables_config[table] = columns

    def __init__(self):
        self.connection_config = self.get_connection_config('../connection_config.txt')
        self.cnx = mysql.connector.connect(**self.connection_config)
        self.cursor = self.cnx.cursor(buffered=True)
        self.query = ""
        self.init_tables_config()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cnx:
            self.cnx.close()


def main():
    pass

if __name__ == '__main__':
    main()
