from MysqlConnector import MysqlConnector
from TextCleaner import TextCleaner
class StructuredDataInserter:

    mysqlc= MysqlConnector()

    def get_data(self,table,columns):
        query=self.mysqlc.select_query(columns=columns,table=table)
        data=self.mysqlc.execute_query(query, returns=True)
        return data

    def clean_text(self,txt):
        txtc = TextCleaner(txt=txt)
        txtc.clear_text()
        raw_text=txtc.get_text()
        return raw_text

    def process_json(self,json_value):
        pass

    def send_data(self,table,data,dictionary):
        self.mysqlc.insert_to_table(table=table,values=data,dictionary=dictionary)

def main():
    sdi = StructuredDataInserter()
    medium_columns='id,entry_id,text'
    medium_table='rss_medium'
    data = sdi.get_data(medium_table,medium_columns)
    structured_columns=['id_rss_medium','link','main_text']
    structured_table='structured_data'
    dicts=[]
    clean_text=[]
    for x in data:
       t=sdi.clean_text(x[2])
       clean_text.append(t)

    for i,x in enumerate(data):
        dicts.append({structured_columns[0]:x[0],structured_columns[1]:x[1],structured_columns[2]:clean_text[i]})

    for dic in dicts:
         sdi.send_data(structured_table,dic,dictionary=True)

if __name__ == '__main__':
    main()