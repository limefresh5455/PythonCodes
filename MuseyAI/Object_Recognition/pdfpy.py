import camelot
tables = camelot.read_pdf('/new pdfs/DPP7 route sheets 08.13.2023.pdf')
print(tables)
# tables
# <TableList n=1>
# tables.export('foo.csv', f='csv', compress=True) # json, excel, html, markdown, sqlite
# tables[0]
# <Table shape=(7, 7)>
# tables[0].parsing_report