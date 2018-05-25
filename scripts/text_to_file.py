from StructuredDataInserter import StructuredDataInserter

sdi =StructuredDataInserter()

data = sdi.get_data('rss_entries','id,text')
for row in data:
    sdi.write_to_file(row[1],loc="../res/main_txt/rss_entries/",iterator=row[0])