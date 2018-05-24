from StructuredDataInserter import StructuredDataInserter

sdi = StructuredDataInserter()
medium_columns = 'id,entry_id,text'
medium_table = 'rss_entries'

data = sdi.get_data(medium_table, medium_columns)
structured_columns = ['id_rss_entries', 'link', 'main_text']
structured_table = 'structured_data'
dicts = []
clean_text = []

for x in data:
    t = sdi.clean_text(x[2])
    clean_text.append(t)

for i, x in enumerate(data):
    dicts.append({structured_columns[0]: x[0], structured_columns[1]: x[1], structured_columns[2]: clean_text[i]})

for dic in dicts:
    sdi.send_data(structured_table, dic, dictionary=True)