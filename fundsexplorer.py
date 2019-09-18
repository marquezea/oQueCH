import csv
import bs4
import requests
import sqlite3
from urllib.request import urlopen

def parseSite():
    # set URL to be opened
    myUrl = 'https://www.fundsexplorer.com.br/ranking'

    # open web page and get HTML data
    with requests.Session() as s:
        r = s.get(myUrl)
        page_html_raw = r.content

        mySoup = bs4.BeautifulSoup(page_html_raw,'html.parser')

        # decode the parsed html into elements
        myTable = mySoup.find('table', attrs={ 'id' : 'table-ranking'})
        #myHeaders = [header.text for header in myTable.find_all('th')]
        myHeaders = ['CODIGO','SETOR','PRECO_ATUAL','LIQ_DIARIA','DIVIDEND','DIVIDENT_YIELD','DY_3M_ACUM','DY_6M_ACUM','DY_12M_ACUM','DY_3M_MEDIA','DY_6M_MEDIA','DY_12M_MEDIA','DY_ANO','VAR_PRECO','RENTAB_PERIODO','RENTAB_ACUM','PATRIM_LIQ','VPA','P_VPA','DY_PATRIMONIAL','VAR_PATRIMONIAL','RENTAB_PATR_PERIODO','RENTAB_PATR_ACUM','VACANCIA_FISICA','VACANCIA_FINANCEIRA','QTDE_ATIVOS']

        myRows = []
        myRows.append(myHeaders)
        for row in myTable.tbody.find_all('tr'):
            uRow = [val.text for val in row.find_all('td')]
            for i in range(26):
                if (i>=2):
                   uRow[i] = uRow[i].replace('R$ ','').replace('.','').replace(',','.').replace('.',',').replace('N/A','')
            myRows.append(uRow)

        print(myRows)
        return myRows

# create SQLITE DB
cmd = """INSERT INTO FIIS VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

with sqlite3.connect("stocks.db") as conn:
    # Create the table if it doesn't exist.
    conn.execute(
        """CREATE TABLE IF NOT EXISTS FIIS(
                CODIGO string,
                SETOR string,
                PRECO_ATUAL number,
                LIQ_DIARIA number,
                DIVIDEND number,
                DIVIDENT_YIELD number,
                DY_3M_ACUM number,
                DY_6M_ACUM number,
                DY_12M_ACUM number,
                DY_3M_MEDIA number,
                DY_6M_MEDIA number,
                DY_12M_MEDIA number,
                DY_ANO number,
                VAR_PRECO number,
                RENTAB_PERIODO number,
                RENTAB_ACUM number,
                PATRIM_LIQ number,
                VPA number,
                P_VPA number,
                DY_PATRIMONIAL number,
                VAR_PATRIMONIAL number,
                RENTAB_PATR_PERIODO number,
                RENTAB_PATR_ACUM number,
                VACANCIA_FISICA number,
                VACANCIA_FINANCEIRA number,
                QTDE_ATIVOS number
            );"""
        )

    # delete previous data
    conn.execute('DELETE FROM FIIS')

    # loop all sectors
    retRows = parseSite()
    
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True, delimiter='\t')

    f = open('fiis.csv','w', newline='', encoding='utf-8')
    writer = csv.writer(f, dialect='myDialect')
    for row in retRows:
        writer.writerow(row)
    f.close()

    for row in retRows:
        conn.execute(cmd, row)




